#!/bin/bash
#SBATCH --job-name=msa_focal_protein
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lwoods@tgen.org
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH --time=5-00:00:00
#SBATCH -c 16
#SBATCH --output=tmp/metaflow/bp3c50id/focal_protein/msa.%j.log

# Create log directory
mkdir -p tmp/metaflow/bp3c50id/focal_protein

# Run Metaflow workflow for MSA focal protein
cd workflows
python linear_epitope_flow.py run \
    --dset-name bp3c50id \
    --workflow-type msa_focal