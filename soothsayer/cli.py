"""soothsayer CLI — the checking engine the Soothsayer skills call.

    soothsayer version
    soothsayer init [path]                     initialise a git-backed store
    soothsayer add-evidence --store P --file rec.json
    soothsayer gate --store P [--frozen map.json] [--horizon YYYY-MM-DD] [--max-age N]
    soothsayer check-tree tree.json            /sooth-tree: partition + sum
    soothsayer check-workplan workplan.json    /sooth-workplan: kill conditions + tolerances
    soothsayer check-synthesis synth.json --store P   /sooth-synthesize: traceability
    soothsayer demo                            self-contained demonstration
"""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .artifacts import GhostPack, IssueTree, Synthesis
from .gates import FrozenFetcher, gate_records
from .models import EvidenceRecord
from .skillgates import ghost_pack_gate, traceability_gate, tree_partition_gate
from .store import Store


def _print_results(results: list) -> int:
    failed = 0
    for r in results:
        mark = "PASS" if r.passed else "FAIL"
        if not r.passed:
            failed += 1
        line = f"  [{mark}] {r.gate}"
        print(line)
        for reason in r.reasons:
            print(f"         - {reason}")
    print(f"\n{len(results) - failed}/{len(results)} gates passed.")
    return failed


def cmd_version(_args) -> int:
    print(f"soothsayer {__version__}")
    return 0


def cmd_init(args) -> int:
    Store(args.path).init()
    print(f"initialised store at {args.path}")
    return 0


def cmd_add_evidence(args) -> int:
    rec = EvidenceRecord.from_dict(json.loads(open(args.file, encoding="utf-8").read()))
    path = Store(args.store).init().add_evidence(rec)
    print(f"added {rec.id} -> {path}")
    return 0


def cmd_gate(args) -> int:
    store = Store(args.store)
    records = store.evidence()
    if not records:
        print("no evidence in store")
        return 0
    fetcher = None
    if args.frozen:
        mapping = json.loads(open(args.frozen, encoding="utf-8").read())
        fetcher = FrozenFetcher(mapping)
    results = gate_records(
        records, fetcher=fetcher, decision_horizon=args.horizon, max_age_days=args.max_age
    )
    return 1 if _print_results(results) else 0


def cmd_demo(_args) -> int:
    from .demo import run_demo

    return run_demo()


def cmd_check_tree(args) -> int:
    tree = IssueTree.from_dict(json.loads(open(args.file, encoding="utf-8").read()))
    return 1 if _print_results([tree_partition_gate(tree)]) else 0


def cmd_check_workplan(args) -> int:
    pack = GhostPack.from_dict(json.loads(open(args.file, encoding="utf-8").read()))
    return 1 if _print_results([ghost_pack_gate(pack)]) else 0


def cmd_check_synthesis(args) -> int:
    synth = Synthesis.from_dict(json.loads(open(args.file, encoding="utf-8").read()))
    known = set(Store(args.store).evidence_by_id().keys())
    return 1 if _print_results([traceability_gate(synth, known)]) else 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="soothsayer", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("version").set_defaults(func=cmd_version)

    pi = sub.add_parser("init")
    pi.add_argument("path", nargs="?", default=".soothsayer")
    pi.set_defaults(func=cmd_init)

    pa = sub.add_parser("add-evidence")
    pa.add_argument("--store", required=True)
    pa.add_argument("--file", required=True)
    pa.set_defaults(func=cmd_add_evidence)

    pg = sub.add_parser("gate")
    pg.add_argument("--store", required=True)
    pg.add_argument("--frozen", help="JSON map of url -> source text")
    pg.add_argument("--horizon", help="decision horizon date YYYY-MM-DD")
    pg.add_argument("--max-age", type=int, default=365)
    pg.set_defaults(func=cmd_gate)

    sub.add_parser("demo").set_defaults(func=cmd_demo)

    pt = sub.add_parser("check-tree")
    pt.add_argument("file")
    pt.set_defaults(func=cmd_check_tree)

    pw = sub.add_parser("check-workplan")
    pw.add_argument("file")
    pw.set_defaults(func=cmd_check_workplan)

    ps = sub.add_parser("check-synthesis")
    ps.add_argument("file")
    ps.add_argument("--store", required=True)
    ps.set_defaults(func=cmd_check_synthesis)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
