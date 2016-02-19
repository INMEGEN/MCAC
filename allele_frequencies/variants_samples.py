import vcf
import os
from pprint import pprint

from samples import vcf_probands


variants = {}

sample_ids = set()

for path in vcf_probands:
    with open(path) as f:
        vcfr = vcf.Reader(f)
        sample = vcfr.samples[0]
        sample_ids.add(sample)
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
                    
                    if GMAF:
                        vkey = "%s:%s_%s/%s" % (chrom,v.POS,v.REF,v.ALT)
                        if not vkey in variants:
                            variants[vkey] = {'symbol'  : SYMBOL,
                                              'existing': Existing_variation,
                                              'gmaf'    : GMAF,
                                              'het'     : set(),
                                              'hom'     : set(),
                            }

                        if v.num_het == 0:
                            variants[vkey]['hom'].add(sample)
                        else:
                            variants[vkey]['het'].add(sample)


print ";".join(["vkey","symbol","existing","gmaf"] + [sid for sid in sample_ids])

for v in variants:
    row = [v,
           variants[v]['symbol'],
           variants[v]['existing'],
           variants[v]['gmaf']]
    for sample in sample_ids:
        if sample in variants[v]['het']:
            row.append('1')
        elif sample in variants[v]['hom']:
            row.append('2')
        else:
            row.append('0')

    print ";".join( row )

              
