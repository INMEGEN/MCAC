import csv
import argparse


from pprint import pprint

parser = argparse.ArgumentParser(description='Generate a VCF with the intersection of the variants of input VCFs')
parser.add_argument('--files', type=argparse.FileType('r'), nargs='+', required=True )
parser.add_argument('--intersection', type=argparse.FileType('w'), required=True )
args   = parser.parse_args()


variants = {}

for f in args.files:
    csvr = csv.reader( f, delimiter='\t' )
    for l in csvr:
        if not l[0].startswith('#'):
            (Uploaded_variation, Location, Allele, Gene, Feature, Feature_type, Consequence, cDNA_position, CDS_position, Protein_position, Amino_acids, Codons, Existing_variation, Extra) = l
            extraslist = Extra.split(';')
            extras = {'SYMBOL': '-'}
            for e in extraslist:
                (k,v) = e.split('=')
                extras[k] = v

            if f.name in variants:
                variants[f.name].update([(Location, Gene, Existing_variation, Consequence, extras['SYMBOL'])])
            else:
                variants[f.name] = set([(Location, Gene, Existing_variation, Consequence, extras['SYMBOL'])])


    
candidates = set.intersection( *variants.values() )


for v in candidates:
    args.intersection.write("\t".join(v)+"\n")
                                                                        
