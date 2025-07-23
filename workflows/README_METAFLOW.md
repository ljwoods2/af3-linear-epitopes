# Metaflow Linear Epitope Workflows

This directory contains the Metaflow-based replacement for the previous Nextflow workflows.

## Structure

- `linear_epitope_flow.py`: Main Metaflow workflow definition
- `scripts_metaflow/`: SLURM job scripts that launch Metaflow workflows for different datasets

## Usage

### Running Individual Workflow Steps

The main workflow supports different workflow types:

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

### Running with SLURM

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

## Migration from Nextflow

This Metaflow implementation replaces the previous Nextflow workflows with equivalent functionality:

| Nextflow File | Metaflow Equivalent |
|---------------|-------------------|
| `00_clean_raw_data.*.nf` | `--workflow-type clean` |
| `02_msa_focal_protein.nf` | `--workflow-type msa_focal` |  
| `02_msa_peptide.nf` | `--workflow-type msa_peptide` |
| `03_inference_focal_protein.nf` | `--workflow-type inference_focal` |
| `03_inference_peptide.nf` | `--workflow-type inference_peptide` |
| `04_bepipred_focal_protein.nf` | `--workflow-type bepipred` |
| `06_extract_conf.nf` | `--workflow-type extract_conf` |

## Environment Setup

Ensure Metaflow is installed:

```bash
pip install metaflow
```

Or use the updated conda environment that includes Metaflow:

```bash
conda env create --name linear-epitope --file envs/env.yaml
```