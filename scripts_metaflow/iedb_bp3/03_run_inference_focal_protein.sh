#!/bin/bash
#SBATCH --job-name=inference_focal_protein
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lwoods@tgen.org
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH --time=5-00:00:00
#SBATCH -c 16
#SBATCH --output=tmp/metaflow/iedb_bp3/focal_protein/inference.%j.log

# Create log directory
mkdir -p tmp/metaflow/iedb_bp3/focal_protein

# Run Metaflow workflow for inference focal protein
cd workflows
python linear_epitope_flow.py run \
    --dset-name iedb_bp3 \
    --workflow-type inference_focal