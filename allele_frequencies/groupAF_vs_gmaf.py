import vcf
import os
from pprint import pprint

from samples import vcf_probands_complete_wide_hlplx as vcf_probands

variants = {}
samples = set()
for path in vcf_probands:
    with open(path) as f:
        vcfr = vcf.Reader(f)
        sample = "s_%s" % vcfr.samples[0]
        samples.add(sample)

        for v in vcfr:
            if 'CSQ' in v.INFO:
                for csq in v.INFO['CSQ']:
                    (Allele,Consequence,IMPACT,SYMBOL,Gene,Feature_type,Feature,
                     BIOTYPE,EXON,INTRON,HGVSc,HGVSp,cDNA_position,CDS_position,
                     Protein_position,Amino_acids,Codons,Existing_variation,DISTANCE,
                     STRAND,VARIANT_CLASS,SYMBOL_SOURCE,HGNC_ID,CANONICAL,TSL,CCDS,
                     ENSP,SWISSPROT,TREMBL,UNIPARC,SIFT,PolyPhen,DOMAINS,GMAF,
                     AFR_MAF,AMR_MAF,ASN_MAF,EAS_MAF,EUR_MAF,SAS_MAF,AA_MAF,EA_MAF,
                     CLIN_SIG,SOMATIC,PHENO,PUBMED,MOTIF_NAME,MOTIF_POS,HIGH_INF_POS,MOTIF_SCORE_CHANGE) = csq.split('|')

                    chrom = v.CHROM
                    if chrom.find('chr') == -1:
                        chrom = 'chr' + chrom
                    
                    if not GMAF:
                        GMAF = 'N.D.'
                        
                    vkey = "%s:%s_%s/%s" % (chrom,v.POS,v.REF,v.ALT)
                    if not vkey in variants:
                        variants[vkey] = {'symbol'  : SYMBOL,
                                          'existing': Existing_variation,
                                          'Protein_position' : Protein_position,
                                          'Amino_acids' : Amino_acids,
                                          'gmaf'    : GMAF,
                                          'AFR_MAF' : AFR_MAF,
                                          'AMR_MAF' : AMR_MAF,
                                          'ASN_MAF' : ASN_MAF,
                                          'EAS_MAF' : EAS_MAF,
                                          'EUR_MAF' : EUR_MAF,
                                          'SAS_MAF' : SAS_MAF,
                                          'AA_MAF'  : AA_MAF,
                                          'EA_MAF'  : EA_MAF,
                                          'het'     : set(),
                                          'hom'     : set(),
                                      }

                    if v.num_het == 0:
                        variants[vkey]['hom'].add(sample)
                    else:
                        variants[vkey]['het'].add(sample)

samples = list(samples)

print ";".join(["vkey","existing",'Protein_position','Amino_acids',
                "gmaf",'AFR_MAF','AMR_MAF','ASN_MAF','EAS_MAF','EUR_MAF','SAS_MAF','AA_MAF','EA_MAF',
                "het","hom","het_count", "hom_count"]+samples)

for v in variants:
    row = [v,
           variants[v]['existing'],
           variants[v]['Protein_position'],           
           variants[v]['Amino_acids'],
           variants[v]['gmaf'],
           variants[v]['AFR_MAF'],
           variants[v]['AMR_MAF'],
           variants[v]['ASN_MAF'],
           variants[v]['EAS_MAF'],
           variants[v]['EUR_MAF'],
           variants[v]['SAS_MAF'],
           variants[v]['AA_MAF'],
           variants[v]['EA_MAF'],
           ",".join(variants[v]['het']),
           ",".join(variants[v]['hom']),
           str(len(variants[v]['het'])),
           str(len(variants[v]['hom']))]

    for s in samples:
        if s in variants[v]['het']:
            alleles = '1'
        elif s in variants[v]['hom']:
            alleles = '2'
        else:
            alleles = '0'
        row.append(alleles)
    print ";".join(row)
              
