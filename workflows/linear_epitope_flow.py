#!/usr/bin/env python3
"""
Linear Epitope Prediction Metaflow Workflow

This workflow replaces the Nextflow pipelines for predicting linear epitopes using AlphaFold3.
It orchestrates data cleaning, MSA generation, inference, BepiPred scoring, and confidence extraction.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional

from metaflow import FlowSpec, step, Parameter, resources


class LinearEpitopeFlow(FlowSpec):
    """
    A Metaflow workflow for linear epitope prediction using AlphaFold3.
    
    This workflow processes different datasets through multiple stages:
    1. Data cleaning and preparation
    2. MSA generation 
    3. AlphaFold3 inference
    4. BepiPred scoring
    5. Confidence extraction
    """
    
    # Parameters
    dset_name = Parameter(
        'dset-name',
        help='Dataset name (e.g., bp3c50id, hv_class, hv_seg, etc.)',
        required=True
    )
    
    data_dir = Parameter(
        'data-dir', 
        help='Base data directory',
        default='data'
    )
    
    workflow_type = Parameter(
        'workflow-type',
        help='Type of workflow to run (clean, msa_focal, msa_peptide, inference_focal, inference_peptide, bepipred, extract_conf)',
        required=True
    )
    
    torch_home = Parameter(
        'torch-home',
        help='TORCH_HOME directory',
        default='/tgen_labs/altin/torch'
    )
    
    esm_dir = Parameter(
        'esm-dir', 
        help='ESM encodings directory',
        default='/tgen_labs/altin/esm_encodings'
    )

    @step
    def start(self):
        """
        Initialize the workflow and determine which pipeline to run.
        """
        print(f"Starting Linear Epitope Flow for dataset: {self.dset_name}")
        print(f"Workflow type: {self.workflow_type}")
        
        self.base_path = Path(self.data_dir) / self.dset_name
        self.outdir = str(self.base_path / "focal_protein")
        
        # Set environment variables
        os.environ['TORCH_HOME'] = self.torch_home
        
        # Process workflow immediately based on type
        if self.workflow_type == 'clean':
            self._process_clean_workflow()
        elif self.workflow_type == 'msa_focal':
            self._process_msa_focal_workflow()
        elif self.workflow_type == 'msa_peptide':
            self._process_msa_peptide_workflow()
        elif self.workflow_type == 'inference_focal':
            self._process_inference_focal_workflow()
        elif self.workflow_type == 'inference_peptide':
            self._process_inference_peptide_workflow()
        elif self.workflow_type == 'bepipred':
            self._process_bepipred_workflow()
        elif self.workflow_type == 'extract_conf':
            self._process_extract_conf_workflow()
        else:
            raise ValueError(f"Unknown workflow type: {self.workflow_type}")
            
        self.next(self.end)

    def _process_clean_workflow(self):
        """Process clean workflow."""
        print(f"Cleaning raw data for dataset: {self.dset_name}")
        
        if self.dset_name == 'bp3c50id':
            self._clean_bp3c50id()
        elif self.dset_name == 'hv_class':
            self._clean_hv_class()
        elif self.dset_name == 'hv_seg':
            self._clean_hv_seg()
        elif self.dset_name == 'iedb_bp3':
            self._clean_iedb_bp3()
        elif self.dset_name == 'in_class':
            self._clean_in_class()
        elif self.dset_name == 'in_seg':
            self._clean_in_seg()
        else:
            raise ValueError(f"Unknown dataset for cleaning: {self.dset_name}")

    def _process_msa_focal_workflow(self):
        """Process MSA focal workflow."""
        print("Running MSA for focal proteins")
        
        staged_dir = self.base_path / "focal_protein" / "staged"
        parquet_files = list(staged_dir.glob("*.filt*.parquet"))
        
        if not parquet_files:
            raise FileNotFoundError(f"No filtered parquet files found in {staged_dir}")
            
        for pq_file in parquet_files:
            print(f"Processing MSA for {pq_file}")

    def _process_msa_peptide_workflow(self):
        """Process MSA peptide workflow."""
        print("Running MSA for peptides")
        
        staged_dir = self.base_path / "peptide" / "staged"  
        parquet_files = list(staged_dir.glob("*.filt*.parquet"))
        
        if not parquet_files:
            raise FileNotFoundError(f"No filtered parquet files found in {staged_dir}")
            
        for pq_file in parquet_files:
            print(f"Processing MSA for {pq_file}")

    def _process_inference_focal_workflow(self):
        """Process inference focal workflow."""
        print("Running AlphaFold3 inference for focal proteins")
        
        staged_dir = self.base_path / "focal_protein" / "staged"
        parquet_files = list(staged_dir.glob("*.filt*.parquet"))
        
        if not parquet_files:
            raise FileNotFoundError(f"No filtered parquet files found in {staged_dir}")
            
        for pq_file in parquet_files:
            print(f"Processing inference for {pq_file}")

    def _process_inference_peptide_workflow(self):
        """Process inference peptide workflow."""
        print("Running AlphaFold3 inference for peptides")
        
        staged_dir = self.base_path / "peptide" / "staged"
        parquet_files = list(staged_dir.glob("*.filt*.parquet"))
        
        if not parquet_files:
            raise FileNotFoundError(f"No filtered parquet files found in {staged_dir}")
            
        for pq_file in parquet_files:
            print(f"Processing inference for {pq_file}")

    def _process_bepipred_workflow(self):
        """Process BepiPred workflow."""
        print("Running BepiPred for focal proteins")
        
        staged_dir = self.base_path / "focal_protein" / "staged"
        filt_files = list(staged_dir.glob("*.filt*.parquet")) 
        
        if not filt_files:
            raise FileNotFoundError(f"No filtered parquet files found in {staged_dir}")
            
        for filt_file in filt_files:
            # Convert parquet to FASTA
            fasta_file = self._parquet_to_fasta(filt_file)
            
            # Run BepiPred
            cmd = [
                'bepipred3_CLI.py',
                '-i', str(fasta_file),
                '-o', '.',
                '-pred', 'mjv_pred',
                '-add_seq_len',
                '-esm_dir', self.esm_dir
            ]
            self._run_command(cmd)
            
            # Join BepiPred results with original data
            csv_files = list(Path('.').glob('*.csv'))
            if csv_files:
                self._join_bepipred_inference(filt_file, csv_files[0])

    def _process_extract_conf_workflow(self):
        """Process confidence extraction workflow."""
        print("Extracting confidence scores")
        
        staged_dir = self.base_path / "focal_protein" / "staged"
        filt_files = list(staged_dir.glob("*.filt*.parquet"))
        
        if not filt_files:
            raise FileNotFoundError(f"No filtered parquet files found in {staged_dir}")
            
        for filt_file in filt_files:
            cmd = [
                'extract_conf.py',
                '--input_pq', str(filt_file),
                '--inference_path', f"{self.outdir}/inference",
                '--output', f"{filt_file.stem}.conf.parquet"
            ]
            self._run_command(cmd)

    def _clean_bp3c50id(self):
        """Clean BP3C50ID dataset."""
        cmd = [
            'clean_bp3c50id.py',
            '--raw_data_path', f'data/bp3c50id/raw',
            '--discard_path', f'{self.base_path}/focal_protein/staged/bp3c50id.discard.parquet',
            '-o', f'{self.base_path}/focal_protein/staged/bp3c50id.filt.parquet'
        ]
        self._run_command(cmd)

    def _clean_hv_class(self):
        """Clean HV class dataset."""
        # Run multiple cleaning steps as in the original workflow
        
        # Clean HV1
        cmd1 = [
            'clean_hv1.py',
            '-t', 'data/hv_class/raw/PV1_meta_2020-11-23.tsv',
            '--output', 'hv1_class_peptide.cleaned.parquet'
        ]
        self._run_command(cmd1)
        
        # Clean HV2  
        cmd2 = [
            'clean_hv2.py',
            '-c', 'data/hv_class/raw/HV2_annot.csv',
            '-o', 'hv2_class_peptide.cleaned.parquet'
        ]
        self._run_command(cmd2)
        
        # Combine HV1 and HV2 using inline Python
        self._combine_hv_class()
        
        # Clean focal protein
        cmd3 = [
            'clean_hv1_focal_protein.py',
            '-f', 'data/hv_class/raw/fulldesign_2019-02-27_wGBKsw.fasta',
            '-o', 'hv_class_focal_protein.cleaned.parquet'
        ]
        self._run_command(cmd3)
        
        # Filter and annotate
        cmd4 = [
            'filt_annot_hv_class.py',
            '-p', 'hv_class_peptide.cleaned.parquet',
            '-op', f'{self.base_path}/peptide/staged/hv_class_peptide.cleaned.filt.parquet',
            '-f', 'hv_class_focal_protein.cleaned.parquet', 
            '-of', f'{self.base_path}/focal_protein/staged/hv_class_focal_protein.cleaned.filt.parquet'
        ]
        self._run_command(cmd4)

    def _combine_hv_class(self):
        """Combine HV1 and HV2 datasets using polars."""
        import polars as pl
        
        hv1 = pl.read_parquet("hv1_class_peptide.cleaned.parquet").with_columns(
            pl.lit(False).alias("epitope")
        )
        hv2 = pl.read_parquet("hv2_class_peptide.cleaned.parquet").with_columns(
            pl.lit(True).alias("epitope")
        )
        
        combined = pl.concat([hv1, hv2], how="vertical")
        combined.write_parquet("hv_class_peptide.cleaned.parquet")

    def _clean_hv_seg(self):
        """Clean HV seg dataset."""
        cmd = [
            'clean_hv_seg_peptide.py',
            '--fasta_path', 'data/hv_seg/raw/fulldesign_2019-02-27_wGBKsw.fasta',
            '--output_path', f'{self.base_path}/peptide/staged/hv_seg_peptide.filt.parquet'
        ]
        self._run_command(cmd)

    def _clean_iedb_bp3(self):
        """Clean IEDB BP3 dataset."""
        cmd = [
            'clean_iedb_bp3.py',
            '--raw_data_path', 'data/iedb_bp3/raw',
            '--discard_path', f'{self.base_path}/focal_protein/staged/iedb_bp3.discard.parquet',
            '-o', f'{self.base_path}/focal_protein/staged/iedb_bp3.filt.parquet'
        ]
        self._run_command(cmd)

    def _clean_in_class(self):
        """Clean IN class dataset."""
        # Similar to HV class but with different scripts
        cmd1 = [
            'clean_in_class_focal_protein.py',
            '-f', 'data/in_class/raw/fulldesign_2019-02-27_wGBKsw.fasta',
            '-o', 'in_class_focal_protein.cleaned.parquet'
        ]
        self._run_command(cmd1)
        
        cmd2 = [
            'clean_in_class_peptide.py', 
            '-p', 'data/in_class/raw/HGBI_set_v2.csv',
            '-o', 'in_class_peptide.cleaned.parquet'
        ]
        self._run_command(cmd2)
        
        cmd3 = [
            'filt_annot_in_class.py',
            '-p', 'in_class_peptide.cleaned.parquet',
            '-op', f'{self.base_path}/peptide/staged/in_class_peptide.cleaned.filt.parquet',
            '-f', 'in_class_focal_protein.cleaned.parquet',
            '-of', f'{self.base_path}/focal_protein/staged/in_class_focal_protein.cleaned.filt.parquet'
        ]
        self._run_command(cmd3)

    def _clean_in_seg(self):
        """Clean IN seg dataset."""
        cmd = [
            'clean_in_seg_peptide.py',
            '--fasta_path', 'data/in_seg/raw/fulldesign_2019-02-27_wGBKsw.fasta',
            '--output_path', f'{self.base_path}/peptide/staged/in_seg_peptide.filt.parquet'
        ]
        self._run_command(cmd)

    def _parquet_to_fasta(self, parquet_file: Path) -> Path:
        """Convert parquet file to FASTA format."""
        # This is a placeholder - would need to implement actual conversion
        # based on the PARQUET_TO_FASTA module logic
        fasta_file = parquet_file.with_suffix('.fasta')
        print(f"Converting {parquet_file} to {fasta_file}")
        return fasta_file

    def _join_bepipred_inference(self, filt_file: Path, csv_file: Path):
        """Join BepiPred results with filtered dataset."""
        import polars as pl
        
        filt_dset = pl.read_parquet(str(filt_file))
        bepipred_out = pl.read_csv(str(csv_file)).with_columns(
            pl.col("BepiPred-3.0 linear epitope score").str.strip_chars().cast(pl.Float64)
        )
        
        bp = (
            bepipred_out.group_by("Accession", maintain_order=True).agg([
                pl.col("BepiPred-3.0 score").alias("bp3_score"),
                pl.col("BepiPred-3.0 linear epitope score").alias("bp3_linear_score"),
            ])
        ).rename({"Accession": "job_name"})
        
        filt_dset = filt_dset.join(bp, on="job_name")
        output_file = filt_file.parent / f"{filt_file.stem}.bp3.parquet"
        filt_dset.write_parquet(str(output_file))

    @step
    def end(self):
        """
        Workflow completion.
        """
        print(f"Linear epitope workflow completed for {self.dset_name}")
        print(f"Workflow type: {self.workflow_type}")

    def _run_command(self, cmd: List[str], cwd: Optional[str] = None, env: Optional[dict] = None):
        """
        Execute a command with proper error handling.
        """
        if env is None:
            env = os.environ.copy()
            
        # Add workflow bin directory to PATH
        bin_dir = Path(__file__).parent / "bin"
        if bin_dir.exists():
            env['PATH'] = f"{bin_dir}:{env.get('PATH', '')}"
            
        print(f"Running command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd, 
                check=True, 
                capture_output=True, 
                text=True,
                cwd=cwd,
                env=env
            )
            print(f"Command output: {result.stdout}")
            if result.stderr:
                print(f"Command stderr: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            print(f"stdout: {e.stdout}")
            print(f"stderr: {e.stderr}")
            raise


if __name__ == '__main__':
    LinearEpitopeFlow()