"""Tests for the shared provider-registry primitive (pass-4 C2).

browser/web_search/image_gen registries used to hand-copy the same
registration/locking/snapshot machinery; they now delegate to
``agent.provider_registry.ProviderRegistry``. These tests pin the generic
contract the three adapters share so a future change to the primitive is
verified once for all families.
"""

from __future__ import annotations

from agent.provider_registry import ProviderRegistry


class _FakeProvider:
    def __init__(self, name: str):
        self.name = name


def test_register_and_get_global():
    r = ProviderRegistry(family="test")
    p = _FakeProvider("alpha")
    r.register_provider(p)
    assert r.get_provider("alpha") is p
    assert r.get_provider("missing") is None


def test_get_prefers_scoped_over_global():
    r = ProviderRegistry(family="test")
    global_p = _FakeProvider("same")
    scoped_p = _FakeProvider("same")
    r.register_provider(global_p)
    r.register_provider(scoped_p, scope="profile-a")
    assert r.get_provider("same", scope="profile-a") is scoped_p
    assert r.get_provider("same") is global_p


def test_list_sorted_and_merged():
    r = ProviderRegistry(family="test")
    b = _FakeProvider("bravo")
    a = _FakeProvider("alpha")
    r.register_provider(b)
    r.register_provider(a, scope="profile-a")
    names = [p.name for p in r.list_providers(scope="profile-a")]
    assert names == ["alpha", "bravo"]


def test_snapshot_restore_identity_guard():
    r = ProviderRegistry(family="test")
    old = _FakeProvider("old")
    new = _FakeProvider("old")  # same key, different instance (hot-reload)
    r.register_provider(old)
    assert r.snapshot_registration("old") is old
    # Restore only when *current* is still installed.
    assert r.restore_registration("old", current=new, previous=None) is False
    r.register_provider(new)
    assert r.restore_registration("old", current=new, previous=None) is True
    assert r.get_provider("old") is None


def test_reset_bumps_generation_monotonically():
    r = ProviderRegistry(family="test")
    r.register_provider(_FakeProvider("x"))
    g1 = r.registry_generation()
    r.reset_for_tests()
    g2 = r.registry_generation()
    assert g2[0] > g1[0]  # monotonic, not zeroed (historic contract)
    assert r.list_providers() == []


def test_type_check_enforced():
    r = ProviderRegistry(family="test", type_check=lambda p: hasattr(p, "name"))
    r.register_provider(_FakeProvider("ok"))
    import pytest

    with pytest.raises(TypeError):
        r.register_provider(object())  # type: ignore[arg-type]