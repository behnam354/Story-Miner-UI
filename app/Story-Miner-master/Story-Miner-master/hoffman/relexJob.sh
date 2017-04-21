#!/bin/bash
#$ -l h_data=4G,h_rt=11:00:00
#$ -o $HOME/job_output.txt
#$ -e $HOME/job_errors.txt
#$ -t 1-2:1
. /u/local/Modules/default/init/modules.sh

dataset="Vaccination/mothering_chunks"

projectDataDir="$HOME/relation_extraction/data"
projectDir="$HOME/relation_extraction"
outdir="$projectDataDir/output"

inputFile1="$projectDataDir/${dataset}/sents_$((4*${SGE_TASK_ID}-3)).txt"
inputFile2="$projectDataDir/${dataset}/sents_$((4*${SGE_TASK_ID}-2)).txt"
inputFile3="$projectDataDir/${dataset}/sents_$((4*${SGE_TASK_ID}-1)).txt"
inputFile4="$projectDataDir/${dataset}/sents_$((4*${SGE_TASK_ID})).txt"

outputDir="$outdir/"

module load python/2.7
python $projectDir/re_behnam/final_version_relex/relEx_parse_tree.py $inputFile1 $outputDir &
python $projectDir/re_behnam/final_version_relex/relEx_parse_tree.py $inputFile2 $outputDir &
python $projectDir/re_behnam/final_version_relex/relEx_parse_tree.py $inputFile3 $outputDir &
python $projectDir/re_behnam/final_version_relex/relEx_parse_tree.py $inputFile4 $outputDir &

echo "Tasks $((4*${SGE_TASK_ID}-3))-$((4*${SGE_TASK_ID})) started."

