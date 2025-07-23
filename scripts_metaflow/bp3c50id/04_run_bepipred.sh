#!/bin/bash
#SBATCH --job-name=bepipred
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lwoods@tgen.org
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH -c 8
#SBATCH --time=2-00:00:00
#SBATCH --gres=gpu:1
#SBATCH --output=tmp/metaflow/bp3c50id/focal_protein/bepipred.%j.log

# Create log directory
mkdir -p tmp/metaflow/bp3c50id/focal_protein

# Run Metaflow workflow for BepiPred
cd workflows
python linear_epitope_flow.py run \
    --dset-name bp3c50id \
    --workflow-type bepipred