# JLISS Controlled Simulation Reproducibility Package

This package contains the regenerated synthetic controlled-simulation dataset supporting the revised JLISS manuscript.

### Contents

- `simulation_parameters.json` — explicit simulation parameters and provenance notes.
- `generate_jliss_simulation.py` — deterministic reconstruction generator.
- `JLISS_regenerated_controlled_simulation_300.csv` — regenerated 300-record dataset.
- `RECONSTRUCTION_NOTE.md` — provenance and wording guidance.
- `JLISS_archived_reference_dataset_300.xlsx` — is the archived synthetic dataset.

### Scope

The dataset is synthetic and controlled. It is not a set of live hotel observations, physical IoT measurements, or 300 live Ethereum Sepolia confirmation measurements.

The Ethereum Sepolia deployment and demonstration transactions in the manuscript remain separate implementation evidence.

### Reproduce

```bash
python generate_jliss_simulation.py
```

The generator uses the fixed random seed in `simulation_parameters.json` and produces the same 300-record CSV deterministically.
