
# Linear epitope prediction using AlphaFold3

## Setup

Create a .env file in the project root:

```bash
CONDA_PREFIX=/path/to/conda/installation
```

Swap the path in `envs/env.yaml` to the project root to your cloned path:

```yaml
...
  - pip:
    # swap me for git URL
    - /path/to/cloned/repo
...
```

Install the nextflow and project environments:

```bash
# project environment
conda env create --name <name> --file envs/env.yaml
# nf-core/nextflow env 
conda env create --name <name> --file envs/nf-core.yaml
```
