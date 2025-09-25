# Bachelor's Thesis: Interpretable Openproblems

Openproblems provides us a living benchmark, however the results of that benchmark are often difficult to interpret. In this thesis we aim to define better ways of interpreting benchmark results from the batch integration task.

* [openproblems batch integration task](https://github.com/openproblems-bio/task_batch_integration)

## Praktische Arbeit

- literature search
    
    [Reading list](https://www.notion.so/Reading-list-1d58252fc2f9804383cfcfe81737c787?pvs=21)
    
- understand openproblems infrastructure
- add new integration methods to batch integration task
    - DRVI, (sysVI, scPoli)
    - other methods from other lab, scMerge
- investigate metrics
    - Add existing published metrics
        - **ASW improved**
        - Lutge et al. paper **CellMixS**
        - **(kSIM)**
    - check how scIB metrics differ from these on existing open problems datasets
- analyse 1 dataset in detail
    - ~~HLCA,~~ mouse pancreas
    - look at biology beyond cell type

### Deliverables

- Add 1 method and 1 metric to OP
- prototype investigation of integration results on 1 dataset
- written project proposal of the research plan of the thesis
- ~~intermediate presentation~~

## Translation of Open problems to single-cell analysis workflows

- **Main questions:**
    1. *How can you **translate** open problems results to best practices?*
    2. *How can we **interpret** open problems results and their **generalization** to unseen use cases (datasets)?*
        1. How do we interpret differences in metric-based ranking
        2. Can we predict how a method will work on a new dataset?
- **Scope:** Case-study on batch integration task

### **Work package 0: Add training data**

- add Archmap datasets & existing integrations from HCA integration team
- Conceptualize which dataset characteristics you want to log as predictors of integration performance
- Target: 10 more datasets

### Work package 1: Metrics evaluation - Are we evaluating good performance correctly?

- scib metrics
    - how do they correspond to ~~our~~ data? get this info from the papers directly
    - e.g. **ASW**, but we have nested batch
    - e.g. cell-type based metrics - do large scores also come from good cell type separation, rare celltypes
- Range of scIB metrics
    - similar to feature selection metrics selection https://doi.org/10.1038/s41592-025-02624-3
    - correlation of metrics, range, how useful are metrics compared to others?
- How can we improve interpretability of the benchmark results?
    - Improved documentation of metrics
    - Case study of integrated object vs metrics (Work package 3)
- Show limitation of x metrics
    - follow up with a potential  improvement
    - don’t reinvent the wheel

### Work package 2: Predict model performance

- Build a predictor on dataset features → Can we predict model performance from dataset features?
    - check Robrecht’s trajectory paper on order of testing datasets
    - small N large K problem
- Which characteristics do we want to use?
    - correlated characteristics
- What aspects of the datasets are more important for the integration?

### Work package 3: Manual evaluation

Evaluate integration performance by analysing real dataset (e.g. CxG datasets already considered in the openproblems benchmark)

- show that the ranking via scib metrics corresponds to what a biologist might expect in their data
- show whether there is an improvement of new metrics with regard to
- show if there is an improvement in clustering of the top-performing method vs the worst-performing method
