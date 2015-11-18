import vcf
from pprint import pprint

vcfdir = '/home/rgarcia/MCAC/vcf/'

samples = [ 'caem_fvi_rigo/S01','caem_fvi_rigo/S02','caem_fvi_rigo/S03','caem_fvi_rigo/S04','caem_fvi_rigo/S07',
            '500/S24', '500/S34', '500/S42' ]

vars = {}
for sample in samples:
    path = "%s/%s.vcf" % (vcfdir, sample)
    f = open(path, 'r')
    vars[sample] = set()
    vcfr = vcf.Reader( f )
    for v in vcfr:
        variant = "%s:%s %s/%s" % (v.CHROM, v.POS, v.REF, v.ALT)
        vars[sample].add(variant)

        
caem = set.union(vars['caem_fvi_rigo/S01'], vars['500/S34'])
hset = set.union(vars['caem_fvi_rigo/S02'], vars['500/S24'])
keet = set.union(vars['caem_fvi_rigo/S03'], vars['500/S42'])

controls = set.union(vars['caem_fvi_rigo/S07'], vars['caem_fvi_rigo/S04'])

interesting = set.intersection(caem, hset, keet) - controls

with open( '%s/caem_fvi_rigo/S01.vcf' % vcfdir, 'r' ) as inhandle, \
     open('%s/family_filtered_exm_halo_CAEMiHSETiKEET-7u4.vcf' % vcfdir, 'w') as outhandle:
    invcf   = vcf.Reader( inhandle )
    outvcf  = vcf.Writer( outhandle, invcf )

    for v in invcf:
        variant = "%s:%s %s/%s" % (v.CHROM, v.POS, v.REF, v.ALT)
        if variant in interesting:
            outvcf.write_record(v)    

