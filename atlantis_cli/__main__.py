from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__
from .agent import (
    build_contract,
    initialize_agent,
    plan_agent,
    resolve_root,
    verify_agent,
)
from .config import load_agent_registry
from .corn import (
    build_context_receipt,
    forge_projection_plan,
    format_corn_report,
    tick_corn,
    validate_corn,
)
from .doctor import doctor_json, format_doctor, run_doctor
from .experience import create_experience_receipt, format_experience, validate_experience
from .help_mode import build_help, format_help, format_interfaces, list_interfaces
from .links import check_markdown_links, format_link_report
from .lineage import (
    format_lineage_report,
    inspect_lineage_receipt,
    validate_lineage_contract,
)
from .note import create_note
from .release import format_release, validate_release
from .sphere_dos import boot_sphere_dos, format_sphere_dos, sphere_dos_status
from .status_map import format_status_maps, validate_status_maps
from .tutorial import format_tutorial, start_tutorial
from .versioning import (
    classify_connection,
    format_connection,
    format_version_report,
    validate_version_contract,
)
from .workspace import (
    format_workspace_report,
    initialize_workspace,
    workspace_plan,
    workspace_status,
)


def _add_workspace_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--component",
        action="append",
        default=[],
        help="対象component ID。複数指定可能。省略時は全component。",
    )
    parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    parser.add_argument("--json", action="store_true", help="JSONで出力する。")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atlantis",
        description="SphereOS Atlantisの文書・環境契約を補助する従属CLI",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    doctor_parser = commands.add_parser("doctor", help="環境を変更せずに診断する。")
    doctor_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    doctor_parser.add_argument("--json", action="store_true", help="JSONで出力する。")
    doctor_parser.add_argument(
        "--require-container",
        action="store_true",
        help="container runtime未検出をfailにする。",
    )

    links_parser = commands.add_parser("links", help="Markdownのrepository内参照をoffline検査する。")
    links_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    links_parser.add_argument("--json", action="store_true", help="JSONで出力する。")

    agent_parser = commands.add_parser("agent", help="コードエージェントの拘束付き初期化を行う。")
    agent_commands = agent_parser.add_subparsers(dest="agent_command", required=True)
    for name, help_text in (
        ("detect", "provider CLIを実行せず、PATH上の存在だけを検出する。"),
        ("plan", "生成予定のsession contractを表示する。"),
        ("init", "モデルを呼ばずsession contractだけを生成する。"),
        ("verify", "生成済みcontractと現行policy hashを検証する。"),
    ):
        subparser = agent_commands.add_parser(name, help=help_text)
        subparser.add_argument("--provider", action="append", default=[], help="provider ID。複数指定可能。")
        subparser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
        subparser.add_argument("--json", action="store_true", help="JSONで出力する。")
        if name == "init":
            subparser.add_argument("--refresh", action="store_true", help="差分のある生成済みcontractを更新する。")

    workspace_parser = commands.add_parser(
        "workspace",
        help="固定revisionから複数repository workspaceを計画・展開する。",
    )
    workspace_commands = workspace_parser.add_subparsers(
        dest="workspace_command",
        required=True,
    )
    for name, help_text in (
        ("status", "networkを使わず、component配置とrevisionを検査する。"),
        ("plan", "既存pathを変更せず、必要な展開actionを表示する。"),
        ("init", "networkを明示使用し、不足componentだけを固定revisionでcloneする。"),
    ):
        subparser = workspace_commands.add_parser(name, help=help_text)
        _add_workspace_arguments(subparser)

    sphere_dos_parser = commands.add_parser(
        "sphere-dos",
        help="standalone runtimeではないSphere-DOS開発shellを扱う。",
    )
    sphere_dos_commands = sphere_dos_parser.add_subparsers(
        dest="sphere_dos_command",
        required=True,
    )
    sphere_boot_parser = sphere_dos_commands.add_parser(
        "boot",
        help="local開発sessionとreceiptを生成する。modelやcomponent runtimeは起動しない。",
    )
    sphere_boot_parser.add_argument("--world", help="使用するworld profile ID。")
    sphere_boot_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    sphere_boot_parser.add_argument("--json", action="store_true", help="JSONで出力する。")
    sphere_status_parser = sphere_dos_commands.add_parser(
        "status",
        help="現在のlocal開発sessionを読み取り専用で表示する。",
    )
    sphere_status_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    sphere_status_parser.add_argument("--json", action="store_true", help="JSONで出力する。")

    corn_parser = commands.add_parser(
        "corn",
        help="repository-nativeなwork itemとcontext closureを扱う。",
    )
    corn_commands = corn_parser.add_subparsers(dest="corn_command", required=True)
    corn_validate_parser = corn_commands.add_parser(
        "validate",
        help="CORN registry、work item、eventをoffline検証する。",
    )
    corn_validate_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    corn_validate_parser.add_argument("--json", action="store_true", help="JSONで出力する。")
    corn_context_parser = corn_commands.add_parser(
        "context",
        help="required sourceを解決し、context hash receiptを作る。",
    )
    corn_context_parser.add_argument("--work-item", required=True, help="CORN work item ID。")
    corn_context_parser.add_argument(
        "--write-capsule",
        action="store_true",
        help="正本ではないcontext capsule cacheを.atlantisへ書く。",
    )
    corn_context_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    corn_context_parser.add_argument("--json", action="store_true", help="JSONで出力する。")
    corn_tick_parser = corn_commands.add_parser(
        "tick",
        help="scheduler互換のone-shot activation receiptを生成する。",
    )
    corn_tick_parser.add_argument("--work-item", required=True, help="CORN work item ID。")
    corn_tick_parser.add_argument("--reason", required=True, help="activation reason。")
    corn_tick_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    corn_tick_parser.add_argument("--json", action="store_true", help="JSONで出力する。")
    corn_forge_parser = corn_commands.add_parser(
        "forge-plan",
        help="Forge projectionをnetworkなしで計画する。",
    )
    corn_forge_parser.add_argument("--work-item", required=True, help="CORN work item ID。")
    corn_forge_parser.add_argument("--adapter", required=True, help="Forge adapter ID。")
    corn_forge_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    corn_forge_parser.add_argument("--json", action="store_true", help="JSONで出力する。")

    note_parser = commands.add_parser("note", help="未確定のブレストや観測をnoteへ保存する。")
    note_commands = note_parser.add_subparsers(dest="note_command", required=True)
    new_parser = note_commands.add_parser("new", help="雛形から衝突安全なnoteを作成する。")
    new_parser.add_argument("--title", required=True, help="noteの題名。")
    new_parser.add_argument("--shelf", required=True, help="note/registry.jsonに登録した棚。")
    new_parser.add_argument("--kind", default="brainstorm", help="note/registry.jsonに登録した種別。")
    new_parser.add_argument("--scope", default="未整理。", help="対象・範囲の初期値。")
    new_parser.add_argument("--exclusions", default="未整理。", help="除外範囲の初期値。")
    new_parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="公開可能なsource。複数指定できる。秘密値を渡さない。",
    )
    new_parser.add_argument(
        "--authoring-agent",
        default="human-or-unspecified",
        help="作成主体。認証情報やsession IDを含めない。",
    )
    new_parser.add_argument(
        "--clock-calibration",
        default="unverified",
        choices=("calibrated", "unverified", "unknown"),
        help="ホスト時計の校正状態。既定は未確認。",
    )
    new_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    new_parser.add_argument("--dry-run", action="store_true", help="予定pathだけを表示し、書き込まない。")
    new_parser.add_argument(
        "--timestamp",
        help="作成時刻の上書き。import・fixture用ISO 8601値。通常は指定しない。",
    )
    new_parser.add_argument(
        "--persona",
        action="append",
        default=[],
        help="本人が自己申告したpersona／立場。複数指定可能。",
    )
    new_parser.add_argument(
        "--position-statement",
        default="not-declared",
        help="公開を選んだ信仰告白またはposition。推定値を渡さない。",
    )
    new_parser.add_argument(
        "--claim-scope",
        default="not-declared",
        help="このNoteの主張射程。",
    )
    new_parser.add_argument(
        "--non-authority-scope",
        default="not-declared",
        help="裁定しない宗派、World、対象。",
    )
    new_parser.add_argument(
        "--memory-publication-consent",
        choices=("not-used", "confirmed"),
        default="not-used",
        help="会話memory由来の公開情報を含まない場合not-used、本人確認済みの場合confirmed。",
    )

    tutorial_parser = commands.add_parser(
        "tutorial",
        help="自己申告personaから非越権な参加入口を解決する。",
    )
    tutorial_commands = tutorial_parser.add_subparsers(
        dest="tutorial_command",
        required=True,
    )
    tutorial_start_parser = tutorial_commands.add_parser(
        "start",
        help="persona registryからtutorial入口と必読sourceを計画する。",
    )
    tutorial_start_parser.add_argument(
        "--persona",
        action="append",
        required=True,
        help="本人が自己申告したpersona。複数指定可能。",
    )
    tutorial_start_parser.add_argument(
        "--route",
        default="auto",
        help="auto、help、note-only、full-development。",
    )
    tutorial_start_parser.add_argument(
        "--proficiency",
        default="unknown",
        choices=("unknown", "newcomer", "explorer", "contributor", "maintainer"),
        help="本人が明示した習熟度。既定はunknown。personaから推定しない。",
    )
    tutorial_start_parser.add_argument(
        "--intent",
        default="look-around",
        choices=("look-around", "learn", "write-note", "report-experience", "inspect", "implement"),
        help="今回の意図。既定はlook-around。実装開始にはimplementの明示が必要。",
    )
    tutorial_start_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    tutorial_start_parser.add_argument("--json", action="store_true", help="JSONで出力する。")

    help_parser = commands.add_parser(
        "help",
        help="習熟度を推定せず、現在能力と参加入口を読み取り専用で案内する。",
    )
    help_parser.add_argument(
        "--persona",
        action="append",
        default=[],
        help="本人が自己申告したpersona。省略可能、複数指定可能。",
    )
    help_parser.add_argument(
        "--proficiency",
        default="unknown",
        choices=("unknown", "newcomer", "explorer", "contributor", "maintainer"),
        help="本人が明示した習熟度。既定はunknown。",
    )
    help_parser.add_argument(
        "--intent",
        default="look-around",
        choices=("look-around", "learn", "write-note", "report-experience", "inspect", "implement"),
        help="案内してほしい意図。実装開始にはimplementの明示が必要。",
    )
    help_parser.add_argument(
        "--state",
        choices=("AVAILABLE-NOW", "SCAFFOLDED", "NOT-IMPLEMENTED", "NOT-TESTED", "RESOURCE-WAIT", "UNKNOWN"),
        help="表示する能力状態を絞り込む。",
    )
    help_parser.add_argument(
        "--detail",
        default="summary",
        choices=("summary", "all"),
        help="既定summaryは利用可能入口だけを表示し、allで全状態を明示表示する。",
    )
    help_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    help_parser.add_argument("--json", action="store_true", help="JSONで出力する。")

    capabilities_parser = commands.add_parser(
        "capabilities",
        help="現在能力を状態付きで読み取り専用表示する。",
    )
    capabilities_parser.add_argument(
        "--state",
        choices=("AVAILABLE-NOW", "SCAFFOLDED", "NOT-IMPLEMENTED", "NOT-TESTED", "RESOURCE-WAIT", "UNKNOWN"),
        help="表示する能力状態を絞り込む。",
    )
    capabilities_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    capabilities_parser.add_argument("--json", action="store_true", help="JSONで出力する。")

    interfaces_parser = commands.add_parser(
        "interfaces",
        help="Prompt Line／Command Lineとexecution envelopeの境界を読み取り専用表示する。",
    )
    interfaces_parser.add_argument(
        "--id",
        help="machine ID（prompt-lineまたはcommand-line）で表示を絞り込む。",
    )
    interfaces_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    interfaces_parser.add_argument("--json", action="store_true", help="JSONで出力する。")

    experience_parser = commands.add_parser(
        "experience",
        help="UX上の違和感や楽しさをExperience Receiptとして扱う。",
    )
    experience_commands = experience_parser.add_subparsers(
        dest="experience_command",
        required=True,
    )
    experience_new_parser = experience_commands.add_parser(
        "new",
        help="生の体験表現を潰さず、新しいreceiptを作る。",
    )
    experience_new_parser.add_argument("--summary", required=True, help="短い要約。")
    experience_new_parser.add_argument(
        "--signal", action="append", required=True, help="本人の体験表現。複数指定可能。"
    )
    experience_new_parser.add_argument(
        "--self-cluster", action="append", default=[], help="本人が自己申告したcluster。"
    )
    experience_new_parser.add_argument("--world", default="not-declared", help="対象World。")
    experience_new_parser.add_argument("--context", default="not-declared", help="発生context。")
    experience_new_parser.add_argument("--request-cluster-review", action="store_true")
    experience_new_parser.add_argument("--timestamp", help="fixture用ISO 8601時刻。")
    experience_new_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    experience_new_parser.add_argument("--dry-run", action="store_true")
    experience_validate_parser = experience_commands.add_parser(
        "validate", help="registryと保存済みreceiptをoffline検証する。"
    )
    experience_validate_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    experience_validate_parser.add_argument("--json", action="store_true", help="JSONで出力する。")

    lineage_parser = commands.add_parser(
        "lineage",
        help="assetの系譜・非越権・局所extension receiptをoffline検査する。",
    )
    lineage_commands = lineage_parser.add_subparsers(
        dest="lineage_command",
        required=True,
    )
    lineage_validate_parser = lineage_commands.add_parser(
        "validate",
        help="contractと正負fixtureをoffline検証する。",
    )
    lineage_validate_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    lineage_validate_parser.add_argument("--json", action="store_true", help="JSONで出力する。")
    lineage_inspect_parser = lineage_commands.add_parser(
        "inspect",
        help="明示指定したreceipt一件だけを読み取り専用検査する。",
    )
    lineage_inspect_parser.add_argument("--receipt", type=Path, required=True, help="検査するJSON receipt。")
    lineage_inspect_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    lineage_inspect_parser.add_argument("--json", action="store_true", help="JSONで出力する。")

    status_parser = commands.add_parser("status", help="Forge／Quest Mapの状態軸を扱う。")
    status_commands = status_parser.add_subparsers(dest="status_command", required=True)
    status_validate_parser = status_commands.add_parser(
        "validate", help="二つのMapをoffline検証する。"
    )
    status_validate_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    status_validate_parser.add_argument("--json", action="store_true", help="JSONで出力する。")

    release_parser = commands.add_parser("release", help="alpha release候補を扱う。")
    release_commands = release_parser.add_subparsers(dest="release_command", required=True)
    release_validate_parser = release_commands.add_parser(
        "validate", help="release manifest、版数、artifactをoffline検証する。"
    )
    release_validate_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    release_validate_parser.add_argument("--json", action="store_true", help="JSONで出力する。")

    version_parser = commands.add_parser(
        "version",
        help="Sphere三層版数座標とWorld接続境界を扱う。",
    )
    version_commands = version_parser.add_subparsers(dest="version_command", required=True)
    version_validate_parser = version_commands.add_parser(
        "validate",
        help="座標、legacy mapping、接続fixtureをoffline検証する。",
    )
    version_validate_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    version_validate_parser.add_argument("--json", action="store_true", help="JSONで出力する。")
    version_connect_parser = version_commands.add_parser(
        "connect",
        help="fixtureから陸続き／Portal／異因果次元境界を判定する。",
    )
    version_connect_parser.add_argument("--fixture", type=Path, required=True, help="接続fixture JSON。")
    version_connect_parser.add_argument("--json", action="store_true", help="JSONで出力する。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        try:
            result = run_doctor(args.repo_root, args.require_container)
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(doctor_json(result) if args.json else format_doctor(result))
        return 1 if result["overall"] == "fail" else 0

    if args.command == "links":
        try:
            result = check_markdown_links(args.repo_root)
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if args.json
            else format_link_report(result)
        )
        return 1 if result["status"] == "fail" else 0

    if args.command == "agent":
        try:
            root = resolve_root(args.repo_root)
            registry = load_agent_registry(root)
            known = [item["id"] for item in registry["providers"]]
            providers = args.provider or known
            output: list[dict[str, object]] = []
            failed = False
            for provider_id in providers:
                if args.agent_command == "detect":
                    contract = build_contract(root, provider_id)
                    provider = contract["provider"]
                    output.append(
                        {
                            "provider": provider_id,
                            "available": provider["available"],
                            "executable": provider["detected_executable"],
                        }
                    )
                elif args.agent_command == "plan":
                    plan = plan_agent(root, provider_id)
                    output.append(
                        {
                            "provider": provider_id,
                            "available": plan.available,
                            "destination": str(plan.destination),
                            "action": plan.action,
                        }
                    )
                elif args.agent_command == "init":
                    plan = initialize_agent(root, provider_id, args.refresh)
                    output.append(
                        {
                            "provider": provider_id,
                            "available": plan.available,
                            "destination": str(plan.destination),
                            "action": plan.action,
                            "model_invoked": False,
                            "network_access_performed": False,
                        }
                    )
                elif args.agent_command == "verify":
                    ok, message = verify_agent(root, provider_id)
                    failed = failed or not ok
                    output.append({"provider": provider_id, "ok": ok, "message": message})
            if args.json:
                print(json.dumps(output, ensure_ascii=False, indent=2))
            else:
                for item in output:
                    print(json.dumps(item, ensure_ascii=False))
            return 1 if failed else 0
        except (OSError, ValueError) as error:
            parser.error(str(error))

    if args.command == "workspace":
        try:
            if args.workspace_command == "status":
                result = workspace_status(args.repo_root, args.component)
            elif args.workspace_command == "plan":
                result = workspace_plan(args.repo_root, args.component)
            else:
                result = initialize_workspace(args.repo_root, args.component)
        except (OSError, RuntimeError, ValueError) as error:
            parser.error(str(error))
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if args.json
            else format_workspace_report(result)
        )
        return 1 if result.get("blocked") else 0

    if args.command == "sphere-dos":
        try:
            result = (
                boot_sphere_dos(args.repo_root, args.world)
                if args.sphere_dos_command == "boot"
                else sphere_dos_status(args.repo_root)
            )
        except (OSError, RuntimeError, ValueError) as error:
            parser.error(str(error))
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if args.json
            else format_sphere_dos(result)
        )
        return 0

    if args.command == "corn":
        try:
            if args.corn_command == "validate":
                result = validate_corn(args.repo_root)
            elif args.corn_command == "context":
                result = build_context_receipt(
                    args.work_item,
                    args.repo_root,
                    write_capsule=args.write_capsule,
                )
            elif args.corn_command == "tick":
                result = tick_corn(args.work_item, args.reason, args.repo_root)
            else:
                result = forge_projection_plan(
                    args.work_item,
                    args.adapter,
                    args.repo_root,
                )
        except (OSError, RuntimeError, ValueError) as error:
            parser.error(str(error))
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if args.json
            else format_corn_report(result)
        )
        return 1 if result.get("overall") in {"fail", "incomplete"} else 0

    if args.command == "note" and args.note_command == "new":
        try:
            result = create_note(
                title=args.title,
                shelf=args.shelf,
                kind=args.kind,
                scope=args.scope,
                exclusions=args.exclusions,
                sources=args.source,
                authoring_agent=args.authoring_agent,
                clock_calibration=args.clock_calibration,
                repo_root=args.repo_root,
                dry_run=args.dry_run,
                timestamp=args.timestamp,
                personas=args.persona,
                position_statement=args.position_statement,
                claim_scope=args.claim_scope,
                non_authority_scope=args.non_authority_scope,
                memory_publication_consent=args.memory_publication_consent,
            )
        except (OSError, ValueError) as error:
            parser.error(str(error))
        state = "DRY-RUN" if args.dry_run else "CREATED"
        print(f"[{state}] {result.path}")
        return 0

    if args.command == "tutorial" and args.tutorial_command == "start":
        try:
            result = start_tutorial(
                args.persona,
                route=args.route,
                proficiency=args.proficiency,
                intent=args.intent,
                repo_root=args.repo_root,
            )
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if args.json
            else format_tutorial(result)
        )
        return 0

    if args.command in {"help", "capabilities"}:
        try:
            result = build_help(
                personas=args.persona if args.command == "help" else None,
                proficiency=args.proficiency if args.command == "help" else None,
                intent=args.intent if args.command == "help" else None,
                state=args.state,
                detail=args.detail if args.command == "help" else "all",
                repo_root=args.repo_root,
            )
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if args.json
            else format_help(result)
        )
        return 0

    if args.command == "interfaces":
        try:
            result = list_interfaces(interface_id=args.id, repo_root=args.repo_root)
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if args.json
            else format_interfaces(result)
        )
        return 0

    if args.command == "experience":
        try:
            result = (
                create_experience_receipt(
                    summary=args.summary,
                    raw_signals=args.signal,
                    self_clusters=args.self_cluster,
                    world=args.world,
                    context=args.context,
                    request_cluster_review=args.request_cluster_review,
                    timestamp=args.timestamp,
                    repo_root=args.repo_root,
                    dry_run=args.dry_run,
                )
                if args.experience_command == "new"
                else validate_experience(args.repo_root)
            )
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if getattr(args, "json", False)
            else format_experience(result)
        )
        return 1 if result.get("overall") == "fail" else 0

    if args.command == "lineage":
        try:
            result = (
                validate_lineage_contract(args.repo_root)
                if args.lineage_command == "validate"
                else inspect_lineage_receipt(args.receipt, args.repo_root)
            )
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if args.json
            else format_lineage_report(result)
        )
        failed = result.get("overall") == "fail" or result.get("status") == "BLOCK"
        return 1 if failed else 0

    if args.command == "status" and args.status_command == "validate":
        try:
            result = validate_status_maps(args.repo_root)
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if args.json
            else format_status_maps(result)
        )
        return 1 if result["overall"] == "fail" else 0

    if args.command == "release" and args.release_command == "validate":
        try:
            result = validate_release(args.repo_root)
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if args.json
            else format_release(result)
        )
        return 1 if result["overall"] == "fail" else 0

    if args.command == "version":
        try:
            if args.version_command == "validate":
                result = validate_version_contract(args.repo_root)
                failed = result["overall"] == "fail"
                output = format_version_report(result)
            else:
                fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
                result = classify_connection(fixture)
                failed = result["status"] in {"BOTTOM", "UNKNOWN-BLOCKED"}
                output = format_connection(result)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            parser.error(str(error))
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else output)
        return 1 if failed else 0

    parser.error("未対応のcommandです。")
    return 2


if __name__ == "__main__":
    sys.exit(main())
