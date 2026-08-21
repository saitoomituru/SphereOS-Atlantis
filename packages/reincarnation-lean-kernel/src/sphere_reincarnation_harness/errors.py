"""Harness例外階層。production Lean Kernelのauthority判定ではない。"""

from __future__ import annotations


class HarnessError(Exception):
    """Harness共通の基底例外。"""


class UnsafeRootError(HarnessError):
    """明示rootが`/`、user home、repository root、空文字等の禁止rootに該当する。"""


class UnsafeIdentifierError(HarnessError):
    """world/fold/task/lease等のIDがtraversalまたはabsolute pathを含む。"""


class SymlinkEscapeError(HarnessError):
    """symlink解決後のpathがharness root外を指している。"""


class ExistingFileError(HarnessError):
    """既定でsilent overwriteしないfileが既に存在する。"""


class HarnessNotInitializedError(HarnessError):
    """`init`を実行する前に`evaluate`等が呼ばれた。"""


class FixtureError(HarnessError):
    """fixtureがharness_only／canonical_contract／authority境界を満たさない。"""
