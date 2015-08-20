import argparse
import json
import pymongo
from bson.objectid import ObjectId
from pprint import pformat, pprint
from os import path

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import Column, Integer, String, Float, create_engine

# from clinical_data import clinical_data
from model import *

parser = argparse.ArgumentParser(description='Load Variant Effect Prediction MongoDB docs to RDB.')
parser.add_argument('--mongo_url', default='mongodb://localhost:27017/', help="MongoDB URL, default: mongodb://localhost:27017/")
parser.add_argument('--rdb_url', default='sqlite:///consequences.sqlite', help="DB URL, default: sqlite:///consequences.sqlite")
parser.add_argument('--init', choices=['true','false'], default='false', help="create relational database and tables, default: false")
args = parser.parse_args()


##############
# Mongo init #
##############
client = pymongo.MongoClient(args.mongo_url)
mcac   = client.mcac
veps   = mcac.veps


####################
# database connect #
####################
engine = create_engine(args.rdb_url)
Session = sessionmaker(bind=engine)


#############
# init rdb? #
#############
if args.init == 'true':
    Base.metadata.create_all(engine)
session = Session()
    


cterms = {}
for v in veps.find( { '$or': [{ "transcript_consequences.polyphen_prediction" : { '$in' : ["probably_damaging",
                                                                                           "possibly_damaging"]} },
                              {  "transcript_consequences.sift_prediction"     : "deleterious"}] } ):
    
    if 'regulatory_feature_consequences' in v:
        for rfc in v['regulatory_feature_consequences']:
            sample_filename = path.basename(v['vep_json']).split('.')
            sample          = sample_filename[0]

            if 'eas_maf' in rfc:
                eas_maf = rfc['eas_maf']
            else:
                eas_maf = None
                
            if 'sas_maf' in rfc:
                sas_maf = rfc['sas_maf']
            else:
                sas_maf = None
                
            c = {'sample'                : sample,
                 'variant_id'            : v['id'],
                 'chrom'                 : v['seq_region_name'],
                 'start'                 : v['start'],
                 'end'                   : v['end'],
                 'regulatory_feature_id' : rfc['regulatory_feature_id'],
                 'biotype'               : rfc['biotype'],
                 'eas_maf'               : eas_maf,
                 'sas_maf'               : sas_maf,                 
                 'impact'                : rfc['impact'],
                 'variant_allele'        : rfc['variant_allele']}

            if 'colocated_variants' in v:
                for cv in v['colocated_variants']:
                    print 'aa_allele', cv.get('aa_allele')
                    print 'aa_maf', cv.get('aa_maf')
                    print 'afr_allele', cv.get('afr_allele')
                    print 'afr_maf', cv.get('afr_maf')
                    print 'allele_string', cv.get('allele_string')
                    print 'amr_allele', cv.get('amr_allele')
                    print 'amr_maf', cv.get('amr_maf')
                    print 'clin_sig', cv.get('clin_sig')
                    print 'ea_allele', cv.get('ea_allele')
                    print 'ea_maf', cv.get('ea_maf')
                    print 'EAS', cv.get('EAS')
                    print 'end', cv.get('end')
                    print 'eur_allele', cv.get('eur_allele')
                    print 'eur_maf', cv.get('eur_maf')
                    print 'id', cv.get('id')
                    print 'minor_allele', cv.get('minor_allele')
                    print 'minor_allele_freq', cv.get('minor_allele_freq')
                    print 'pubmed', cv.get('pubmed')
                    print 'SAS', cv.get('SAS')
                    print 'somatic', cv.get('somatic')
                    print 'start', cv.get('start')
                    print 'strand', cv.get('strand')

                        
            #consequence = Regulatory_feature_consequence(**c)
            #session.add(consequence)
            #session.commit()

