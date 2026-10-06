# metricscape

An scverse-style package for **exploratory analysis of benchmark metrics over a real or simulated search space**,
generalising the analyses from the `ba_interpretable_opsca` thesis notebooks (OpenProblems batch integration).

A *search space* is a set of points (datasets) described by covariates such as batch imbalance. It can be real
(dataset metadata) or simulated (`metricscape.sim`). Over it you can ask:

- `tl.metric_response` – does a metric drift with a covariate, for real methods or for controls?
- `tl.metric_correlation` / `tl.rank_agreement` – do metrics agree with each other / in method rankings?
- `tl.control_separation` – does a metric rank positive controls above negative controls?
- `pl.response_grid`, `pl.heatmap` – visualise the above.

```python
import metricscape as ms

scores = ms.io.read_scores_yaml("score_uns.yaml", drop_metrics=["kbet", "hvg_overlap"])
ex = ms.MetricExplorer(scores, metadata)       # metadata: dataset_id + covariates
ex.response("batch_imbalance_gc")
ex.control_separation()

# simulated space
space = ms.sim.SearchSpace({"imbalance": (0, 1)}).sample(50)
sim = ms.sim.simulate_scores(space, {("scvi", "ilisi"): lambda s: 0.8 - 0.5 * s["imbalance"]}, noise=0.02)
```

## Install

```bash
pip install -e ".[test]" && pytest
```

Note: this package lives in `metricscape/` of the thesis repo and can be split into its own repository
(`git subtree split -P metricscape`).
