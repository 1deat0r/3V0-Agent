"""Skill-misevolution safety gate ("Practice Makes Unsafe", arXiv 2608.12851).

Self-improving agents turn successful executions into reusable policy (skills,
redo entries, harness changes). An *unsafe success* thereby becomes reusable
after its triggering input disappears. This module gives the conservative,
deterministic half of SafeEvolve's "repair + govern reuse": a classifier that
flags unsafe procedure content BEFORE it is authored into a skill / reused, so
evolution optimizes outcomes AND procedure safety.

Design:
- ``audit(content)`` returns a classification: ``blocking`` (must not author /
  reuse) vs ``caution`` (usable only with explicit human approval) vs clean.
- ``govern_reuse(content, approved=())`` is the reuse gate: a blocking skill is
  never reusable; a caution skill is reusable only when its flagged category is
  explicitly pre-approved; a clean skill is reusable.
- Matching is deterministic (regex on the literal procedure text) — no LLM in
  this gate. The gate is cheap and testable; it is meant to run on every
  skill-authoring / redo-ingestion boundary, not to reason about intent.

This is governance of what self-evolution may WRITE and REUSE, complementing
(not replacing) verification: a procedure can be correct yet unsafe.
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field

# ── Blocking: irreversible / credential-exfil / guard-bypass — reject outright ──
_BLOCKING: list[tuple[str, str]] = [
    ("filesystem_destroy", r"\brm\s+-rf\s+/(\s|$)"),
    ("filesystem_home_destroy", r"\brm\s+-rf\s+(~/|\$HOME/)"),
    ("block_device_destroy", r"\b(mkfs|fdisk|parted|dd)\b[^&\n;]*\b(of=|/dev/sd|/dev/nvme)"),
    ("power_off", r"\b(poweroff|shutdown\s+-h|reboot\s+-f|systemctl\s+poweroff|echo\s+[ob]\s*>\s*/proc/sysrq-trigger)"),
    ("credential_dump", r"(cat|sed|dd)\s+[^\n;']*(\.env|\.netrc|id_rsa|\.secrets)"),
    ("credential_leak_refer", r"\b(print\(|echo\s+\$?)([A-Z_]*API_KEY|[A-Z_]*SECRET|[A-Z_]*TOKEN)\b"),
    ("exfil_pipe_shell", r"curl\s+[^\n]*\|\s*(sh|bash)\b"),
    ("guard_bypass", r"-{1,2}(no-verify|force|yes|assume-yes|-y)\b.*(git\s+push|pip|apt|dnf|yum|rm)"),
    ("policy_disable", r"\b(setenforce\s+0|iptables\s+-F|ufw\s+disable|systemctl\s+stop\s+firewalld)"),
]

# ── Caution: disruptive / privilege-escalating / config-mutating — review first ──
_CAUTION: list[tuple[str, str]] = [
    ("recursive_delete", r"\brm\s+-rf\b"),
    ("privilege_escalate", r"\b(sudo|setpriv|gksudo)\b"),
    ("service_toggle", r"\b(systemctl|service)\s+(stop|restart|disable|mask)\b"),
    ("perms_loosen", r"\bchmod\s+-?[0-7]*\.?[0-7]*7{2}\b|\bchmod\s+-R"),
    ("global_pkg", r"\b(pip|pip3|npm|gem|pear)\s+(install|upgrade|update)\s+(-g|--user|-U)"),
    ("force_branch_rewrite", r"\bgit\s+push\s+(-f|--force)\b"),
    ("raw_exec_from_remote", r"curl\s+[^\n]*-o\s+\S+"),
    ("db_drop", r"\bDROP\s+(TABLE|DATABASE|SCHEMA)\b|\bDELETE\s+FROM\b"),
]


@dataclass
class Audit:
    content: str
    source: str | None = None
    blocking: list[str] = field(default_factory=list)   # matched blocking categories
    caution: list[str] = field(default_factory=list)    # matched caution categories

    @property
    def unsafe(self) -> bool:
        return bool(self.blocking)

    @property
    def needs_approval(self) -> bool:
        return bool(self.caution) and not self.blocking

    @property
    def safe_to_author(self) -> bool:
        return not self.blocking

    def reason(self) -> str:
        if self.blocking:
            return "BLOCKED: " + ", ".join(self.blocking)
        if self.caution:
            return "CAUTION: " + ", ".join(self.caution)
        return "clean"


def audit(content: str, *, source: str | None = None) -> Audit:
    """Classify a procedure for safety before authoring / reuse."""
    a = Audit(content=content, source=source)
    for name, pat in _BLOCKING:
        if re.search(pat, content):
            a.blocking.append(name)
    for name, pat in _CAUTION:
        if re.search(pat, content):
            a.caution.append(name)
    return a


@dataclass
class ReuseDecision:
    reusable: bool
    reason: str
    blocking: list[str]
    caution: list[str]

    @property
    def requires_approval(self) -> bool:
        return bool(self.caution) and not self.reusable


def govern_reuse(content: str, *, approved: tuple[str, ...] = ()) -> ReuseDecision:
    """Reuse gate. ``approved`` = caution categories a human pre-approved."""
    a = audit(content)
    if a.blocking:
        return ReuseDecision(False, f"blocked: {a.reason()}", a.blocking, a.caution)
    outstanding = [c for c in a.caution if c not in approved]
    if outstanding:
        return ReuseDecision(
            False, f"requires approval for: {', '.join(outstanding)}",
            [], outstanding)
    return ReuseDecision(True, "reusable", [], a.caution)