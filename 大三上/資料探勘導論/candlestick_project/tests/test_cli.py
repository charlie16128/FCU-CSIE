import subprocess
import sys


def test_help_lists_all_modes(project_root):
    result = subprocess.run(
        [sys.executable, "main.py", "--help"],
        cwd=project_root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    for mode in (
        "--download",
        "--prepare",
        "--train",
        "--validate",
        "--test",
        "--gui",
        "--all",
    ):
        assert mode in result.stdout


def test_gui_does_not_call_training(monkeypatch, project_root):
    from main import run

    monkeypatch.setattr("src.gui.launch_gui", lambda root: None)
    monkeypatch.setattr(
        "src.pipeline.train_patterns",
        lambda root: (_ for _ in ()).throw(AssertionError("training called")),
    )

    assert run(["--gui"], project_root=project_root) == 0


def test_all_runs_data_stages_in_order_but_not_gui(monkeypatch, project_root):
    from main import run

    calls = []
    for name in (
        "download_data",
        "prepare_data",
        "train_patterns",
        "validate_patterns",
        "test_patterns",
    ):
        monkeypatch.setattr(
            f"src.pipeline.{name}",
            lambda root, stage=name: calls.append(stage),
        )
    monkeypatch.setattr(
        "src.gui.launch_gui",
        lambda root: (_ for _ in ()).throw(AssertionError("GUI called")),
    )

    assert run(["--all"], project_root=project_root) == 0
    assert calls == [
        "download_data",
        "prepare_data",
        "train_patterns",
        "validate_patterns",
        "test_patterns",
    ]
