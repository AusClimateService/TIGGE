#!/bin/bash
#PBS -P xv83
#PBS -q copyq
#PBS -l walltime=10:00:00
#PBS -l mem=20GB
#PBS -l storage=gdata/hh5+gdata/xv83
#PBS -l wd

module use /g/data/hh5/public/modules
module load conda/analysis3-unstable

python3 TIGGE_copyq_job.py
