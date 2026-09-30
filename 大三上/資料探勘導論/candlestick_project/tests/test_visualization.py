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


def test_top10_figures_use_centroids_instead_of_profit_bars(
    tmp_path,
    display_fixture,
):
    from src.visualization import generate_required_figures

    display_fixture["bullish"] = display_fixture["bullish"].drop(
        columns="average_directional_profit"
    )
    display_fixture["bearish"] = display_fixture["bearish"].drop(
        columns="average_directional_profit"
    )

    generated = generate_required_figures(display_fixture, tmp_path)

    assert (tmp_path / "top10_bullish.png") in generated
    assert (tmp_path / "top10_bearish.png") in generated
