# DEPRECATED: Nextflow Execution Scripts

**⚠️ NOTICE: These Nextflow execution scripts have been replaced with Metaflow scripts.**

This directory contains the original shell scripts that launched Nextflow workflows. They are no longer actively used and have been replaced with Metaflow-based execution scripts.

## Migration Information

- **Old system**: Shell scripts in this directory that run `nextflow run`
- **New system**: Shell scripts in `scripts_metaflow/` that run `python linear_epitope_flow.py run`
- **Migration date**: July 2025

## For Current Usage

Please use the new Metaflow execution scripts instead:

```bash
# Use scripts in scripts_metaflow/ directory
sbatch scripts_metaflow/bp3c50id/00_run_clean_raw_data.sh
```

See the main README.md for complete usage instructions.