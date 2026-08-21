"""Tests for TUI gateway slash_worker profile_home propagation (#40677)."""

from pathlib import Path
from unittest.mock import MagicMock, patch


def test_slash_worker_accepts_profile_home():
    """_SlashWorker.__init__ accepts profile_home parameter."""
    # threev0_state evaluates get_ev0_home() / "state.db" at import time, so
    # the mock must return a Path (a bare str raises TypeError under per-file
    # subprocess isolation).
    with patch.dict("sys.modules", {
        "threev0_constants": MagicMock(
            get_threev0_home=MagicMock(return_value=Path("/tmp/ev0_test")),
        ),
    }):
        with patch("subprocess.Popen") as mock_popen:
            mock_popen.return_value.stdout = MagicMock()
            mock_popen.return_value.stderr = MagicMock()

            from tui_gateway.server import _SlashWorker

            # Test initialization with profile_home
            worker = _SlashWorker(
                session_key="test_key",
                model="test-model",
                profile_home="/home/luke/.3V0/profiles/work"
            )

            # Verify Popen was called
            assert mock_popen.called

            # Check that EV0_HOME was set in the environment
            call_kwargs = mock_popen.call_args[1]
            assert "env" in call_kwargs
            assert call_kwargs["env"]["EV0_HOME"] == "/home/luke/.3V0/profiles/work"


