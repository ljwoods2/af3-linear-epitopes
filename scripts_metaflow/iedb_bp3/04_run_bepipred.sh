#!/bin/bash
#SBATCH --job-name=bepipred
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lwoods@tgen.org
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH -c 8
#SBATCH --time=2-00:00:00
#SBATCH --gres=gpu:1
#SBATCH --output=tmp/metaflow/iedb_bp3/focal_protein/bepipred.%j.log

# Create log directory
mkdir -p tmp/metaflow/iedb_bp3/focal_protein

# Run Metaflow workflow for BepiPred
cd workflows
python linear_epitope_flow.py run \
    --dset-name iedb_bp3 \
    --workflow-type bepipred