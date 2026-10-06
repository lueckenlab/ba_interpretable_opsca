import numpy as np

import metricscape as ms


def make():
    space = ms.sim.SearchSpace({"imbalance": (0, 1)}).sample(30)
    resp = {
        ("good", "ilisi"): lambda s: 0.8 - 0.5 * s["imbalance"],
        ("good", "ari"): lambda s: np.full(len(s), 0.7),
        ("embed_cell_types", "ilisi"): lambda s: np.full(len(s), 0.9),
        ("shuffle_integration", "ilisi"): lambda s: np.full(len(s), 0.1),
        ("embed_cell_types", "ari"): lambda s: np.full(len(s), 0.9),
        ("shuffle_integration", "ari"): lambda s: np.full(len(s), 0.1),
    }
    return ms.sim.simulate_scores(space, resp, noise=0.01)


def test_grid():
    assert len(ms.sim.SearchSpace({"a": (0, 1), "b": (0, 1)}).grid(4)) == 16


def test_response_recovers_slope():
    ex = ms.MetricExplorer(make())
    r = ex.response("imbalance").set_index("metric_id")
    assert abs(r.loc["ilisi", "slope"] + 0.5) < 0.1
    assert r.loc["ilisi", "r2"] > 0.9


def test_control_separation_and_corr():
    ex = ms.MetricExplorer(make())
    assert (ex.control_separation() == 1.0).all()
    assert ex.correlation().shape == (2, 2)


def test_read_scores_yaml(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text("- {dataset_id: a/b, method_id: X, metric_ids: [ari, kbet], metric_values: [1.0, null]}\n")
    df = ms.io.read_scores_yaml(p, drop_metrics=["kbet"])
    assert df.to_dict("records") == [{"dataset_id": "b", "method_id": "x", "metric_id": "ari", "metric_value": 1.0}]
