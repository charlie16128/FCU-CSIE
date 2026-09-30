def test_required_figure_names_are_written(tmp_path, display_fixture):
    from src.visualization import generate_required_figures

    generated = generate_required_figures(display_fixture, tmp_path)
    expected = {
        "top10_bullish.png",
        "top10_bearish.png",
        "validation_parameter_search.png",
        "2026_pattern_performance.png",
        "2026_stock_performance.png",
    }

    assert expected == {path.name for path in generated}
    assert expected <= {path.name for path in tmp_path.glob("*.png")}
    assert all(path.stat().st_size > 0 for path in generated)


def test_figure_generation_does_not_modify_input(tmp_path, display_fixture):
    snapshots = {
        key: frame.copy(deep=True) for key, frame in display_fixture.items()
    }

    from src.visualization import generate_required_figures

    generate_required_figures(display_fixture, tmp_path)

    for key, expected in snapshots.items():
        assert display_fixture[key].equals(expected)
