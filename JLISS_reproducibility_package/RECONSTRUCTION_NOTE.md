# JLISS Controlled-Simulation Reproducibility Package

## Provenance

The original historical script used to generate the first synthetic 300-record
dataset was not retained. This package therefore does **not** claim to recover
or reproduce the undocumented historical generator.

The archived dataset used as the numerical reference for the manuscript is
preserved separately as:

`JLISS_archived_reference_dataset_300.xlsx`

This archived file represents the historical synthetic simulation realization
from which the manuscript's reported numerical results and dataset-level
characteristics were derived.

The file:

`JLISS_regenerated_controlled_simulation_300.csv`

is a newly generated reconstruction produced using the explicitly documented
reconstruction parameters and random seed provided in this package.

Because the original historical generator was not retained, the regenerated
dataset is **not claimed to be byte-identical or row-identical** to the archived
reference dataset. Instead, the reconstruction is intended to provide a
transparent and deterministic reproducibility artifact that documents the
simulation assumptions, workload structure, failure schedule, and generation
procedure used for the revised study.

## Relationship Between the Two Datasets

The two datasets have distinct roles:

| Artifact | Role |
|---|---|
| `JLISS_archived_reference_dataset_300.xlsx` | Archived reference realization used for the manuscript's reported numerical results |
| `JLISS_regenerated_controlled_simulation_300.csv` | Newly generated reconstruction based on the documented reconstruction model |
| `simulation_parameters.json` | Explicit reconstruction parameters and provenance metadata |
| `generate_jliss_simulation.py` | Deterministic reconstruction generator |
| `regenerated_metrics.json` | Summary statistics generated from the regenerated dataset |

The archived reference dataset remains the numerical reference for the results
reported in the manuscript. The regenerated dataset is provided to document and
reproduce the explicit reconstruction model and its documented workload
characteristics.

## What Is Fixed

- 300 records total
- 50 records per scenario across six scenarios
- predefined scenario-level latency target means and sample standard deviations
- fixed failure-case schedule and failure stages
- fixed vendor/milestone workload structure
- explicit normal-based latency reconstruction
- explicit record-level gas-price model
- explicit record-level ETH-to-IDR conversion model
- one simulated confirmation endpoint

## What Is Not Claimed

The package does not claim that the undocumented historical dataset originally
used a normal distribution, any particular random seed, or the exact parameter
values documented in this reconstruction package.

The random seed in `simulation_parameters.json` is a **new reconstruction seed**
and is not claimed to be the historical generator seed.

The reconstruction parameters are derived from archived dataset-level
characteristics and are provided for methodological transparency and
reproducibility.

## Recommended Interpretation

The manuscript should distinguish clearly between:

1. the archived reference dataset used for the reported numerical results;
2. the regenerated reconstruction dataset supplied as a reproducibility artifact;
3. the original historical generator, which is no longer available.

The reconstruction package is therefore intended to make the simulation
assumptions and generation procedure explicit without making an unsupported
claim that the original historical generator has been recovered.
