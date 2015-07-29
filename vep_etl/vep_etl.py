import csv
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from pprint import pprint

parser = argparse.ArgumentParser(description='filter vep')
parser.add_argument('--input', type=argparse.FileType('r'), required=True )
parser.add_argument('--db_url', default='sqlite:///mcac_vep.sqlite', help='DB URL, default: sqlite:///mcac_vep.sqlite')
parser.add_argument('--output', type=argparse.FileType('w'), required=True )
args   = parser.parse_args()

variants = []

# will return a malign score from extras dict
def score(extras):
    s = 0
    if extras['SIFT'].startswith('deleterious'):
        s += 3
        
    if extras['SIFT'].startswith('-'):
        s += 0

    if extras['SIFT'].startswith('tolerated'):
        s += -1

        
    if extras['PolyPhen'].startswith('probably'):
        s += 3
        
    if extras['PolyPhen'].startswith('possibly'):
        s += 2

    if extras['PolyPhen'].startswith('unknown') or extras['PolyPhen'].startswith('-'):
        s += 0

    if extras['PolyPhen'].startswith('benign'):
        s += -1
        
    if extras['IMPACT'] == 'HIGH':
        s += 6

    if extras['IMPACT'] == 'MODIFIER':
        s += 1
        
    if extras['CLIN_SIG'].find('pathogenic') != -1:
        s += 3

    return str(s)



# parse and annotate input file
csvr = csv.reader( args.input, delimiter='\t' )
for l in csvr:
    if not l[0].startswith('#'):
        (Uploaded_variation, Location, Allele, Gene, Feature, Feature_type, Consequence, cDNA_position, CDS_position, Protein_position, Amino_acids, Codons, Existing_variation, Extra) = l
        extraslist = Extra.split(';')
        extras = {'SYMBOL'  : '-',
                  'SIFT'    : '-',
                  'PolyPhen': '-',
                  'PUBMED'  : '-',
                  'CLIN_SIG': '-',
                  'GMAF'    : '-',
                  'IMPACT'  : '-',
                  'Amino_acids' : '-',
                  'Codons'  : '-',
        }
        for e in extraslist:
            (k,v) = e.split('=')
            extras[k] = v

        if extras['PolyPhen'].startswith('p') or extras['SIFT'].startswith('del') or extras['IMPACT'] == 'HIGH' or extras['CLIN_SIG'].find('pathogenic') != -1:
            s = score(extras)
            variants.append([s, extras['SIFT'], extras['PolyPhen'], extras['CLIN_SIG'], extras['IMPACT'],
                             Location, Gene, Existing_variation, Consequence, extras['GMAF'], cDNA_position,
                             CDS_position, Protein_position, extras['SYMBOL'], extras['PUBMED'],
                             Amino_acids, Codons,
                             ])



            
####################
# database connect #
####################
engine  = create_engine(args.db_url)
do.Session = sessionmaker(bind=engine)





# here we should load
args.output.write(";".join(['score',
                             'SIFT',
                             'PolyPhen',
                             'CLIN_SIG',
                             'IMPACT',
                             'location',
                             'gene',
                             'existing_variation',
                             'consequence', 'gmaf',
                             'cDNA_position', 'CDS_position', 'Protein_position',
                             'SYMBOL',
                             'PUBMED', 'amino_acids', 'codons'])+"\n" )
for v in variants:
    args.output.write(";".join(v)+"\n")
