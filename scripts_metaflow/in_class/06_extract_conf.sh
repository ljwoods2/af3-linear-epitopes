#!/bin/bash
#SBATCH --job-name=extract_conf
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lwoods@tgen.org
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH -c 1
#SBATCH --time=1:00:00
#SBATCH --output=tmp/metaflow/in_class/focal_protein/extract_conf.%j.log

# Create log directory
mkdir -p tmp/metaflow/in_class/focal_protein

# Run Metaflow workflow for confidence extraction
cd workflows
python linear_epitope_flow.py run \
    --dset-name in_class \
    --workflow-type extract_conf