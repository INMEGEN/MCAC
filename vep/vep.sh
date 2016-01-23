#!/bin/bash

VEP=/home/rgarcia/downloads/ensembl-tools-release-81/scripts/variant_effect_predictor/variant_effect_predictor.pl

VCFDIR=/home/rgarcia/MCAC/vcf


# for SAMPLE in $(seq -f "%02g" 1 48)
# do
#     for BATCH in {500,}
#     do
#         $VEP -i $VCFDIR/$BATCH/S${SAMPLE}.norepeats.vcf -o $VCFDIR/$BATCH/S${SAMPLE}.vep.csv --everything --fork 30 --offline --assembly GRCh37
#     done
# done



# COMPLETE_VCF="family_filtered_PTLiJATEiJIAT-JPAMuLACA.vcf
# family_filtered_PTLiJATE-JPAMuLACA.vcf
# family_filtered_PTLiJATEiJIAT.vcf
# family_filtered_PTLiJATE.vcf"

# COMPLETE_VCF="A01.JATE.haloplex.vcf
# B01.PTL.haloplex.vcf
# C01.JPAM.halople.vcf
# D01.LACA.halople.vcf
# E01.JIAT.halople.vcf"


# for VCF in $COMPLETE_VCF
# do
#     OUT=`basename $VCF .vcf`
#     $VEP -i $VCFDIR/complete/$VCF -o $VCFDIR/complete/${OUT}.vep.csv --everything --fork 30 --offline --assembly GRCh37    
# done


# EXM_ILLUMINA_VCF="family_filtered_JLRLiJLRMiGEL_con_alelos.vcf
# family_filtered_JLRMiYRM_con_alelos.vcf
# family_filtered_JLRLiJLRMiGEL_sin_alelos.vcf
# family_filtered_JLRMiYRM_sin_alelos.vcf"

# EXM_ILLUMINA_VCF="LMG.vcf
# JLRM.vcf
# YRN.vcf"
# # DLA.vcf
# # GEL.vcf
# # GMCA.vcf
# # JLRL.vcf
# # PTL.vcf
# # LMG.vcf"

# for VCF in $EXM_ILLUMINA_VCF
# do
#     OUT=`basename $VCF .vcf`
#     $VEP --force_overwrite -i $VCFDIR/exm_illumina/$VCF -o $VCFDIR/exm_illumina/${OUT}.vep.csv --everything --fork 30 --offline --assembly GRCh37    
# done



#for SAMPLE in $(seq -f "%02g" 1 11)
#do
#    $VEP -i $VCFDIR/caem_fvi_rigo/S${SAMPLE}.vcf -o $VCFDIR/caem_fvi_rigo/S${SAMPLE}.vep.csv --everything --fork 30 --offline --assembly GRCh37
#done



# COMPLETE_EXCLUSIVE="jate-rest.vcf
# jiat-rest.vcf
# jpam-rest.vcf
# laca-rest.vcf
# ptl-rest.vcf"

# for VCF in $COMPLETE_EXCLUSIVE
# do
#     OUT=`basename $VCF .vcf`
#     $VEP -i $VCFDIR/complete/$VCF -o $VCFDIR/complete/${OUT}.vep.csv --everything --fork 30 --offline --assembly GRCh37
# done


#A01.JATE.vcf"
# COMPLETE_COMPLETE="B01.PTL.vcf
# C01.JPAM.vcf
# D01.LACA.vcf
# E01.JIAT.vcf"

# for VCF in $COMPLETE_COMPLETE
# do
#     OUT=`basename $VCF .vcf`
#     $VEP -i $VCFDIR/complete/$VCF -o $VCFDIR/complete/${OUT}.vep.csv --everything --fork 30 --offline --assembly GRCh37
# done




haloplexbasespace="11_S1.vcf
12_S1.vcf
13_S1.vcf
14_S1.vcf
15_S1.vcf
16_S1.vcf
17_S1.vcf
18_S1.vcf
19_S1.vcf
20_S1.vcf
21_S1.vcf
22_S1.vcf
23_S1.vcf
24_S1.vcf
25_S1.vcf
26_S1.vcf
27_S1.vcf
28_S1.vcf
29_S1.vcf
30_S1.vcf
31_S1.vcf
32_S1.vcf
33_S1.vcf
34_S1.vcf
35_S1.vcf
36_S1.vcf
37_S1.vcf
38_S1.vcf
39_S1.vcf
40_S1.vcf
41_S1.vcf
42_S1.vcf
43_S1.vcf
44_S1.vcf
45_S1.vcf
46_S1.vcf
47_S1.vcf
48_S1.vcf
CFOG_S1.vcf
CYDR_S1.vcf
EEPO_S1.vcf
FJGA_S1.vcf
IXH_S1.vcf
JCVM_S1.vcf
JDJM_S1.vcf
JOS_S1.vcf
JSMC_S1.vcf
MJG_S1.vcf
RRR_S1.vcf"

for VCF in $haloplexbasespace
do
    OUT=`basename $VCF .vcf`
    $VEP -i $VCFDIR/haloplex500basespace/$VCF -o $VCFDIR/haloplex500basespace/${OUT}.vep.csv --everything --fork 30 --offline --assembly GRCh37
done
