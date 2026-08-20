from pathlib import Path


def test_windows_native_install_path_docs_match_installer() -> None:
    doc = Path("website/docs/user-guide/windows-native.md").read_text()
    install = Path("scripts/install.ps1").read_text()

    # The launchers live in a dedicated bin/ dir on PATH — NOT the whole
    # venv\Scripts (which would shadow the user's python, #83797).
    assert "%LOCALAPPDATA%\\3v0\\3v0-agent\\bin" in doc
    assert (
        "Get-Command 3v0        # should print "
        "C:\\Users\\<you>\\AppData\\Local\\3v0\\3v0-agent\\bin\\3v0.exe"
    ) in doc
    # Installer exposes $InstallDir\bin, and must copy the launchers into it.
    assert '$ev0Bin = "$InstallDir\\bin"' in install
    assert "3v0.exe" in install and "3v0-acp.exe" in install
    # Guard against a regression back to putting venv\Scripts on PATH.
    assert '$ev0Bin = "$InstallDir\\venv\\Scripts"' not in install
