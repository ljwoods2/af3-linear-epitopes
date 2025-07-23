#!/bin/bash
#SBATCH --job-name=clean_raw_data
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lwoods@tgen.org
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH -c 1
#SBATCH --time=1:00:00
#SBATCH --output=tmp/metaflow/iedb_bp3/clean_raw_data.%j.log

# Create log directory
mkdir -p tmp/metaflow/iedb_bp3

# Run Metaflow workflow for data cleaning
cd workflows
python linear_epitope_flow.py run \
    --dset-name iedb_bp3 \
    --workflow-type clean