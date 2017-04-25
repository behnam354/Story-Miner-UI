#!/bin/bash
#$ -l h_data=16G,h_rt=23:00:00
#$ -pe shared 4
#$ -o $HOME/job_output.txt
#$ -e $HOME/job_errors.txt
#$ -t 1-50:1

. /u/local/Modules/default/init/modules.sh

dataset="Vaccination/mothering_chunks_sent_sep_clean"

projectDataDir="$HOME/relation_extraction/data"
projectDir="$HOME/relation_extraction"
outdir="$projectDataDir/output"

inputFile1="$projectDataDir/${dataset}/sents_$((4*${SGE_TASK_ID}-3)).txt"
inputFile2="$projectDataDir/${dataset}/sents_$((4*${SGE_TASK_ID}-2)).txt"
inputFile3="$projectDataDir/${dataset}/sents_$((4*${SGE_TASK_ID}-1)).txt"
inputFile4="$projectDataDir/${dataset}/sents_$((4*${SGE_TASK_ID})).txt"

outputFile1="$outdir/"
outputFile2="$outdir/"
outputFile3="$outdir/"
outputFile4="$outdir/"

module load python/2.7
python $projectDir/Story-Miner/final_version_relex/relEx_parse_tree.py $inputFile1 $outputFile1 
python $projectDir/Story-Miner/final_version_relex/relEx_parse_tree.py $inputFile2 $outputFile2 
python $projectDir/Story-Miner/final_version_relex/relEx_parse_tree.py $inputFile3 $outputFile3
python $projectDir/Story-Miner/final_version_relex/relEx_parse_tree.py $inputFile4 $outputFile4

echo "Tasks $((4*${SGE_TASK_ID}-3))-$((4*${SGE_TASK_ID})) finished."

