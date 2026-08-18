#!/usr/bin/env python3
"""Register the KSL libraries in the installed KiCad's GLOBAL library tables.

Scans this repository (and the private kicad-nda-libs checkout when one is
found) for `<Lib>_KSL` libraries and reconciles KiCad's global sym-lib-table
and fp-lib-table against them, writing every URI in the `${KSL_ROOT}` /
`${KNL_ROOT}` path-variable form so the tables stay valid when a checkout
moves. Also verifies those variables are registered in kicad_common.json's
`environment.vars`.

    update_kicad_libraries.py            reconcile (add + fix)
    update_kicad_libraries.py --check    report drift only; exit 1 on drift
    update_kicad_libraries.py --prune    also drop *_KSL entries whose library
                                         no longer exists on disk
    update_kicad_libraries.py --set-vars write KSL_ROOT/KNL_ROOT into
                                         kicad_common.json (KiCad closed!)

Scope and safety:

- Only entries whose name ends in `_KSL` are managed. Everything else in the
  tables is preserved byte-for-byte, always.
- An orphaned `_KSL` entry (no such library in either repo) is removed only
  with --prune, and only when its target does not exist on disk either; an
  orphan whose target exists is reported and left alone.
- Writes refuse to run while a KiCad GUI process is alive (KiCad reads the
  tables at startup and rewrites its config on exit, so edits made while it
  runs are lost or invisible). --force overrides. --check never writes.
- Every modified file is first copied to `<file>.bak-<timestamp>` beside it.

Exit codes: 0 clean / changes applied, 1 drift found (--check) or refused
to run, 2 could not run at all.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SUFFIX = "_KSL"
GUI_PROCS = {"kicad", "eeschema", "pcbnew", "kicad.exe", "eeschema.exe", "pcbnew.exe"}
SKIP_DIRS = {"_attic", "datasheets", "skills", "scripts", "hooks"}


def log(msg):
    print(msg)


def fail(msg, code=2):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


# --------------------------------------------------------------------------
# discovery
# --------------------------------------------------------------------------

def ksl_root():
    env = os.environ.get("KSL_ROOT")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parents[1]


def kicad_config_base():
    override = os.environ.get("KICAD_CONFIG_HOME")
    if override:
        return Path(override)
    home = Path.home()
    if sys.platform == "darwin":
        return home / "Library" / "Preferences" / "kicad"
    if os.name == "nt":
        return Path(os.environ.get("APPDATA", home / "AppData" / "Roaming")) / "kicad"
    return Path(os.environ.get("XDG_CONFIG_HOME", home / ".config")) / "kicad"


def kicad_settings_dir(explicit):
    if explicit:
        d = Path(explicit)
        if not d.is_dir():
            fail(f"--config-dir {d} is not a directory")
        return d
    base = kicad_config_base()
    if not base.is_dir():
        fail(f"no KiCad settings found under {base} — is KiCad installed? "
             "(or pass --config-dir)")
    versions = [d for d in base.iterdir()
                if d.is_dir() and re.fullmatch(r"\d+(\.\d+)*", d.name)
                and (d / "kicad_common.json").exists()]
    if not versions:
        fail(f"no versioned KiCad settings dir with kicad_common.json under {base}")
    return max(versions, key=lambda d: tuple(int(x) for x in d.name.split(".")))


def knl_root(common_vars):
    """Probe for the private repo: env var, then KiCad's own vars, then a
    sibling checkout. Returns None when absent — NDA libraries are optional."""
    for cand in (os.environ.get("KNL_ROOT"),
                 common_vars.get("KNL_ROOT"),
                 str(ksl_root().parent / "kicad-nda-libs")):
        if cand and Path(cand).is_dir():
            return Path(cand).resolve()
    return None


def scan_repo(root, var):
    """Find `<Lib>_KSL` libraries in a checkout. Returns
    {name: {"sym": uri or None, "fp": uri or None}} in path-variable form."""
    libs = {}
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name in SKIP_DIRS or d.name.startswith("."):
            continue
        if not d.name.endswith(SUFFIX):
            continue
        sym = d / f"{d.name}.kicad_sym"
        fp = d / f"{d.name}.pretty"
        if not sym.is_file() and not fp.is_dir():
            continue
        libs[d.name] = {
            "sym": f"${{{var}}}/{d.name}/{d.name}.kicad_sym" if sym.is_file() else None,
            "fp": f"${{{var}}}/{d.name}/{d.name}.pretty" if fp.is_dir() else None,
        }
    return libs


def kicad_gui_running():
    try:
        out = subprocess.run(["ps", "-axo", "comm"], capture_output=True,
                             text=True, check=True).stdout
    except Exception:
        return []  # can't tell (e.g. Windows) — proceed, backups still exist
    names = []
    for line in out.splitlines():
        base = os.path.basename(line.strip()).lower()
        if base in GUI_PROCS:
            names.append(base)
    return names


# --------------------------------------------------------------------------
# table surgery (spans, so unmanaged entries stay byte-identical)
# --------------------------------------------------------------------------

def lib_spans(text):
    """Yield (start, end, name, type, uri) for each depth-1 (lib ...) block."""
    spans = []
    depth = 0
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == '"':
            i += 1
            while i < n and text[i] != '"':
                i += 2 if text[i] == "\\" else 1
            i += 1
            continue
        if c == "(":
            if depth == 1 and text[i:i + 4] == "(lib":
                start = i
                d = 0
                j = i
                while j < n:
                    ch = text[j]
                    if ch == '"':
                        j += 1
                        while j < n and text[j] != '"':
                            j += 2 if text[j] == "\\" else 1
                    elif ch == "(":
                        d += 1
                    elif ch == ")":
                        d -= 1
                        if d == 0:
                            break
                    j += 1
                span = text[start:j + 1]
                spans.append((start, j + 1,
                              _field(span, "name"), _field(span, "type"),
                              _field(span, "uri")))
                i = j + 1
                depth += 0
                continue
            depth += 1
        elif c == ")":
            depth -= 1
        i += 1
    return spans


def _field(span, key):
    m = re.search(r'\(%s\s+"((?:[^"\\]|\\.)*)"' % key, span)
    return m.group(1) if m else None


def set_field(span, key, value):
    return re.sub(r'(\(%s\s+")((?:[^"\\]|\\.)*)(")' % key,
                  lambda m: m.group(1) + value + m.group(3), span, count=1)


def expand(uri, roots):
    for var, root in roots.items():
        if root:
            uri = uri.replace("${%s}" % var, str(root))
    return uri


def reconcile(path, kind, desired, roots, prune):
    """Compute the new table text. Returns (new_text, actions, drift)."""
    text = path.read_text()
    spans = lib_spans(text)
    actions = []          # human-readable, diff-style
    drift = False
    edits = []            # (start, end, replacement)
    seen = set()

    for start, end, name, typ, uri in spans:
        if not name or not name.endswith(SUFFIX):
            continue  # not ours — never touched
        want = desired.get(name, {}).get(kind)
        if want:
            seen.add(name)
            new_span = text[start:end]
            if uri != want:
                new_span = set_field(new_span, "uri", want)
                actions.append(f"  ~ {name}: uri {uri!r} -> {want!r}")
                drift = True
            if typ != "KiCad":
                new_span = set_field(new_span, "type", "KiCad")
                actions.append(f"  ~ {name}: type {typ!r} -> 'KiCad'")
                drift = True
            if new_span != text[start:end]:
                edits.append((start, end, new_span))
        else:
            target = Path(expand(uri or "", roots))
            if "${" in expand(uri or "", roots):
                actions.append(f"  ? {name}: unknown variable in uri, left alone")
            elif target.exists():
                actions.append(f"  ? {name}: not in the repos but target exists "
                               "on disk — left alone")
            elif prune:
                line_start = text.rfind("\n", 0, start) + 1
                edits.append((line_start, end + (text[end:end + 1] == "\n"), ""))
                actions.append(f"  - {name}: pruned (library gone: {uri!r})")
                drift = True
            else:
                actions.append(f"  ! {name}: stale (target missing: {uri!r}) — "
                               "would remove with --prune")

    additions = []
    for name in sorted(desired):
        want = desired[name].get(kind)
        if want and name not in seen:
            additions.append(
                f'  (lib (name "{name}")(type "KiCad")(uri "{want}")'
                f'(options "")(descr "KSL library: {name}"))\n')
            actions.append(f"  + {name}: added ({want})")
            drift = True

    new_text = text
    for start, end, repl in sorted(edits, reverse=True):
        new_text = new_text[:start] + repl + new_text[end:]
    if additions:
        close = new_text.rstrip()
        assert close.endswith(")")
        new_text = close[:-1] + "".join(additions) + ")\n"
    return new_text, actions, drift


def sanity_check(old_text, new_text, kind):
    """The rewritten table must parse, and unmanaged entries must survive
    byte-for-byte."""
    old_unmanaged = [old_text[s:e] for s, e, name, *_ in lib_spans(old_text)
                     if not (name or "").endswith(SUFFIX)]
    new_unmanaged = [new_text[s:e] for s, e, name, *_ in lib_spans(new_text)
                     if not (name or "").endswith(SUFFIX)]
    if old_unmanaged != new_unmanaged:
        fail(f"internal error: unmanaged {kind} entries would change — aborting")
    header = "(sym_lib_table" if kind == "sym" else "(fp_lib_table"
    if not new_text.lstrip().startswith(header):
        fail(f"internal error: rewritten {kind} table lost its header")


# --------------------------------------------------------------------------
# kicad_common.json environment variables
# --------------------------------------------------------------------------

def vars_status(common_path, want_vars):
    data = json.loads(common_path.read_text())
    have = (data.get("environment") or {}).get("vars") or {}
    missing = {k: v for k, v in want_vars.items() if have.get(k) != str(v)}
    return data, have, missing


def backup(path, stamp):
    dest = path.with_name(f"{path.name}.bak-{stamp}")
    shutil.copy2(path, dest)
    return dest


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="report drift without writing; exit 1 on drift")
    ap.add_argument("--prune", action="store_true",
                    help="remove managed entries whose library is gone from disk")
    ap.add_argument("--set-vars", action="store_true",
                    help="write KSL_ROOT/KNL_ROOT into kicad_common.json")
    ap.add_argument("--force", action="store_true",
                    help="write even if a KiCad GUI process is running")
    ap.add_argument("--config-dir", metavar="DIR",
                    help="KiCad versioned settings dir (default: autodetect)")
    args = ap.parse_args()

    ksl = ksl_root()
    if not (ksl / "repository.json").exists():
        fail(f"{ksl} does not look like the kicad-shared-libs checkout "
             "(set KSL_ROOT or run from the repo)")
    cfg = kicad_settings_dir(args.config_dir)
    common_path = cfg / "kicad_common.json"
    _, common_vars, _ = vars_status(common_path, {})
    knl = knl_root(common_vars)
    roots = {"KSL_ROOT": ksl, "KNL_ROOT": knl}

    log(f"KiCad settings : {cfg}")
    log(f"KSL_ROOT       : {ksl}")
    log(f"KNL_ROOT       : {knl or '(not found — NDA libraries skipped)'}")

    desired = scan_repo(ksl, "KSL_ROOT")
    if knl:
        for name, uris in scan_repo(knl, "KNL_ROOT").items():
            if name in desired:
                log(f"warning: {name} exists in both repos; using the public one")
            else:
                desired[name] = uris
    n_sym = sum(1 for v in desired.values() if v["sym"])
    n_fp = sum(1 for v in desired.values() if v["fp"])
    log(f"libraries found: {len(desired)} ({n_sym} symbol, {n_fp} footprint)")

    drift = False
    pending = []  # (path, new_text)
    for kind, fname in (("sym", "sym-lib-table"), ("fp", "fp-lib-table")):
        path = cfg / fname
        if not path.exists():
            fail(f"{path} not found — start KiCad once to create it")
        new_text, actions, d = reconcile(path, kind, desired, roots, args.prune)
        log(f"\n{fname}:")
        for a in actions:
            log(a)
        if not d:
            log("  = in sync")
        drift |= d
        if d and new_text != path.read_text():
            sanity_check(path.read_text(), new_text, kind)
            pending.append((path, new_text))

    want_vars = {"KSL_ROOT": ksl}
    if knl:
        want_vars["KNL_ROOT"] = knl
    common_data, have_vars, missing_vars = vars_status(common_path, want_vars)
    log("\nkicad_common.json environment.vars:")
    for k, v in want_vars.items():
        state = "ok" if str(v) == have_vars.get(k) else \
            f"MISSING or wrong (have {have_vars.get(k)!r}, want {str(v)!r})"
        log(f"  {k}: {state}")
    if missing_vars and not args.set_vars:
        log("  -> re-run with --set-vars (KiCad closed) to fix, or use "
            "Preferences > Configure Paths")
    drift |= bool(missing_vars)

    if args.check:
        log(f"\ncheck: {'DRIFT — a write run would change the above' if drift else 'clean'}")
        sys.exit(1 if drift else 0)

    if not pending and not (missing_vars and args.set_vars):
        log("\nnothing to do")
        return

    running = kicad_gui_running()
    if running and not args.force:
        fail(f"KiCad appears to be running ({', '.join(sorted(set(running)))}) — "
             "it reads these tables at startup and rewrites its config on exit, "
             "so close it first (or --force)", code=1)

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    for path, new_text in pending:
        b = backup(path, stamp)
        path.write_text(new_text)
        log(f"\nwrote {path} (backup: {b.name})")
    if missing_vars and args.set_vars:
        b = backup(common_path, stamp)
        common_data.setdefault("environment", {})
        common_data["environment"].setdefault("vars", {})
        if common_data["environment"]["vars"] is None:
            common_data["environment"]["vars"] = {}
        for k, v in want_vars.items():
            common_data["environment"]["vars"][k] = str(v)
        common_path.write_text(json.dumps(common_data, indent=2,
                                          ensure_ascii=False) + "\n")
        log(f"wrote {common_path} (backup: {b.name})")
    log("\ndone — restart KiCad to pick up the changes")


if __name__ == "__main__":
    main()
