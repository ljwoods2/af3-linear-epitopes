# DEPRECATED: Nextflow Workflows

**⚠️ NOTICE: These Nextflow workflows have been replaced with Metaflow.**

This directory contains the original Nextflow workflow files that are no longer actively used. They have been replaced with a Metaflow-based implementation.

## Migration Information

- **Old system**: Nextflow workflows in this directory
- **New system**: Metaflow workflows in `linear_epitope_flow.py`
- **Migration date**: July 2025

## For Current Usage

Please use the new Metaflow workflows instead:

```bash
cd workflows
python linear_epitope_flow.py run --dset-name <dataset> --workflow-type <type>
```

Or use the SLURM scripts in `scripts_metaflow/` directory.

See the main README.md for complete usage instructions.

## Legacy Files

The following files are kept for reference but are no longer used:

- `*.nf` - Nextflow workflow definitions
- `nextflow.config` - Nextflow configuration  
- `modules/` - Nextflow modules
- `subworkflows/` - Nextflow subworkflows
- `bin/` - Script executables (still used by Metaflow)

The Python scripts in `bin/` are still used by the new Metaflow implementation.