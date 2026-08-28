#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repository_root=$(CDPATH= cd -- "$script_dir/.." && pwd)

exec python3 -B -m atlantis_cli experiment "$@" --repo-root "$repository_root"
