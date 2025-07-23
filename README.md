
# Linear epitope prediction using AlphaFold3

## Setup

### Environment Setup

Install the project and workflow environment:

```bash
# project environment with Metaflow
conda env create --name <name> --file envs/env.yaml
```

Update the path in `envs/env.yaml` to point to your cloned repository path:

```yaml
...
  - pip:
    # swap me for git URL or local path
    - /path/to/cloned/repo
...
```

### Configuration

If running on Gemini, ensure that Alphafold MSAs will use your scratch as a tmp directory (some MSA intermediate files are larger than `/tmp` on compute nodes).

Configure Metaflow if needed:

```bash
# Optional: configure Metaflow datastore location
export METAFLOW_DATASTORE_SYSROOT_LOCAL=/path/to/datastore
```

## Workflows

This project uses **Metaflow** for workflow orchestration. The workflows have been migrated from the previous Nextflow implementation.

### Running Workflows

#### Command Line Usage

```bash
cd workflows
python linear_epitope_flow.py run --dset-name <dataset> --workflow-type <type>
```

Where `<dataset>` can be:
- `bp3c50id`
- `hv_class` 
- `hv_seg`
- `iedb_bp3`
- `in_class`
- `in_seg`

And `<type>` can be:
- `clean`: Data cleaning and preparation
- `msa_focal`: MSA generation for focal proteins
- `msa_peptide`: MSA generation for peptides  
- `inference_focal`: AlphaFold3 inference for focal proteins
- `inference_peptide`: AlphaFold3 inference for peptides
- `bepipred`: BepiPred scoring
- `extract_conf`: Confidence extraction

#### SLURM Job Submission

Use the provided shell scripts to submit jobs to SLURM:

```bash
# Clean raw data
sbatch scripts_metaflow/bp3c50id/00_run_clean_raw_data.sh

# Run MSA for focal proteins
sbatch scripts_metaflow/bp3c50id/02_run_msa_focal_protein.sh

# Run inference
sbatch scripts_metaflow/bp3c50id/03_run_inference_focal_protein.sh

# Run BepiPred
sbatch scripts_metaflow/bp3c50id/04_run_bepipred.sh

# Extract confidence
sbatch scripts_metaflow/bp3c50id/06_extract_conf.sh
```

#### Pipeline Execution Order

For a complete analysis, run workflows in this order:

1. **Clean raw data** (`clean`)
2. **Generate MSA** (`msa_focal` or `msa_peptide`)  
3. **Run inference** (`inference_focal` or `inference_peptide`)
4. **Calculate BepiPred scores** (`bepipred`)
5. **Extract confidence** (`extract_conf`)

### Legacy Nextflow Files

The old Nextflow workflows have been replaced with Metaflow. For reference, the original files are still present in the `workflows/` directory but are no longer used:

- `*.nf` files - Original Nextflow workflow definitions
- `scripts/` - Original Nextflow execution scripts  
- `nextflow.config` - Nextflow configuration

For current usage, use the Metaflow workflows described above.