#!/bin/bash
#SBATCH --job-name=msa_peptide
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lwoods@tgen.org
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH --time=5-00:00:00
#SBATCH -c 16
#SBATCH --output=tmp/nextflow/hv/peptide/msa.%j.log


. ./scripts/setup.sh

# env vars
export NXF_LOG_FILE=tmp/nextflow/hv/peptide/msa/nextflow.log
export NXF_CACHE_DIR=tmp/nextflow/hv/peptide/msa/

nextflow run \
    ./workflows/02_msa_peptide.nf \
    -resume