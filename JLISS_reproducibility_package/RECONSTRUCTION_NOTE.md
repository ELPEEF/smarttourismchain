# JLISS Controlled-Simulation Reproducibility Package

## Provenance

The original historical script used to generate the first synthetic 300-record dataset was not retained. This package therefore does **not** claim to be the original generator.

Instead, this package documents a **new, explicit reconstruction of the controlled-simulation protocol** used for the manuscript revision. The regenerated dataset is intended to provide a transparent and deterministic reproducibility artifact.

## What is fixed

- 300 records total
- 50 records per scenario across six scenarios
- predefined scenario-level latency target means and sample SDs
- fixed failure-case schedule and failure stages
- fixed vendor/milestone workload structure
- explicit normal-based latency generation
- explicit record-level gas-price model
- explicit record-level ETH-to-IDR conversion model
- one simulated confirmation endpoint

## What is not claimed

The package does not claim that the undocumented historical dataset originally used a normal distribution, any particular random seed, or the exact parameterization in this package. Those details are reconstruction parameters introduced here for reproducibility.

## Recommended manuscript language

The manuscript should state that the simulation dataset was **regenerated using an explicitly documented reconstruction model** after the original generator was found not to be preserved. The resulting dataset, parameter file, and generator should then be treated as the authoritative reproducibility artifacts for the revised manuscript.
