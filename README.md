# Bachelor's Thesis: Interpretable Openproblems

Openproblems provides us a living benchmark, however the results of that benchmark are often difficult to interpret. In this thesis we aim to define better ways of interpreting benchmark results from the batch integration task.

* [openproblems batch integration task](https://github.com/openproblems-bio/task_batch_integration)

## Praktische Arbeit

- literature search
    
    [Reading list](https://www.notion.so/Reading-list-1d58252fc2f9804383cfcfe81737c787?pvs=21)
    
- understand openproblems infrastructure
- add new integration methods to batch integration task
    - DrVI, sysVI, scPoli
- investigate metrics
    - scib metrics
        - how do they correspond to our data?
        - e.g. ASW, but we have nested batch
        - e.g. cell-type based metrics - do large scores also come from good cell type separation, rare celltypes
    - **Local metrics**
        - cell type specific biological metrics
        - rare cell types
    - extend existing metrics for batch evaluation
        - e.g. NMI, ARI for batch → lower = better
    - add gene-set based metric (hardcoded)
        - evaluate manually
- analyse 1 dataset in detail
    - HLCA
    - look at biology beyond cell type

### Deliverables

- prototype investigation of integration results on 1 dataset
- written project proposal of the research plan of the thesis
- intermediate presentation

## Translation of Openproblems to single-cell analysis workflows

- **Main questions:**
    1. *How can we demonstrate the **usability** of openproblems to day-to-day single cell analysis?*
    2. *How can we improve the **interpretability** of integration task in openproblems?*
- **Scope:** Case-study on batch integration task

### Work package 1: Metrics evaluation

- Range of scIB metrics
    - similar to feature selection metrics selection https://doi.org/10.1038/s41592-025-02624-3
    - correlation of metrics, range, how useful are metrics compared to others?
- How can we improve interpretability of the benchmark results?
    - Improved documentation of metrics
    - Case study of integrated object vs metrics (Work package 3)

### Work package 2: Implementing new metrics

- literature search of existing metrics that we are missing (e.g. kSIM, scGraph)
    - Pegasus package, **kSIM**: https://doi.org/10.1038/s41592-020-0905-x
    - **scGraph**: https://doi.org/10.1101/2024.04.02.587824, https://www.biorxiv.org/content/10.1101/2024.04.02.587824v1.full.pdf
- **Nested batch effect metrics**
    - modified ASW for nested batch effect → **follow up with more nested batch correction evaluations**
    - Would it make sense to develop a new metric dedicated to nested batch effects, maybe even cross system/species?
- **Biologically informed metrics**
    - marker-gene-based metrics with dataset-specific marker genes
    - other dataset-specific gene programs
- **Local metrics**
    - cell type specific biological metrics
- extend existing metrics for batch evaluation
    - e.g. NMI, ARI for batch → lower = better

### Work package 3: Manual evaluation

Evaluate integration performance by analysing real dataset (e.g. CxG datasets already considered in the openproblems benchmark)

- show that the ranking via scib metrics corresponds to what a biologist might expect in their data
- show whether there is an improvement of new metrics with regard to
- show if there is an improvement in clustering of the top-performing method vs the worst-performing method
