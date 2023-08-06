"""
Reference free AF-based demultiplexing on pooled scRNA-seq
Generate genotype information in VCF format
Jon Xu (jun.xu@uq.edu.au)
Lachlan Coin
Aug 2018
"""

import numpy as np
import pandas as pd
from scipy.stats import binom
from scipy.sparse import csr_matrix
import argparse, datetime, csv


def main():

    # Process command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--ref', required=True,  help='Ref count CSV')
    parser.add_argument('-a', '--alt', required=True,  help='Alt count CSV')
    parser.add_argument('-p', '--psc', required=True, help='generated P(S|C)')
    args = parser.parse_args()

    dist_alleles = []
    ref = pd.read_csv(args.ref, header=0, index_col=0)
    alt = pd.read_csv(args.alt, header=0, index_col=0)
    ref_s = csr_matrix(ref.values)
    alt_s = csr_matrix(alt.values)
    all_POS = ref.index

    # get cell assignment
    P_s_c = pd.read_csv(args.psc, header=0, index_col=0)
    A_s_c = ((P_s_c >= 0.9) * 1).astype('float64')
    num = len(P_s_c.columns)

    err = 0.01  # error rate assumption
    # binomial simulation for genotype likelihood P(D|AA,RA,RR) with the alt count vs total count condition and (err, 0.5, 1-err) as allele probability
    lp_d_rr = pd.DataFrame(binom.pmf(pd.DataFrame(alt_s.dot(A_s_c)), pd.DataFrame((alt_s + ref_s).dot(A_s_c)), err), index=all_POS, columns=range(num)).apply(np.log10)
    lp_d_ra = pd.DataFrame(binom.pmf(pd.DataFrame(alt_s.dot(A_s_c)), pd.DataFrame((alt_s + ref_s).dot(A_s_c)), 0.5), index=all_POS, columns=range(num)).apply(np.log10)
    lp_d_aa = pd.DataFrame(binom.pmf(pd.DataFrame(alt_s.dot(A_s_c)), pd.DataFrame((alt_s + ref_s).dot(A_s_c)), 1-err), index=all_POS, columns=range(num)).apply(np.log10)

    vcf_content = pd.DataFrame(index = all_POS, columns = range(-9, num))  # -9~-1: meta data, 0: doublet state, 1:num: samples
    names = vcf_content.columns.tolist()
    names[0] = '#CHROM'
    names[1] = 'POS'
    names[2] = 'ID'
    names[3] = 'REF'
    names[4] = 'ALT'
    names[5] = 'QUAL'
    names[6] = 'FILTER'
    names[7] = 'INFO'
    names[8] = 'FORMAT'
    vcf_content.columns = names
    vcf_content.loc[:,'#CHROM'] = [item.split(':')[0] for item in all_POS]
    vcf_content.loc[:,'POS'] = [item.split(':')[1] for item in all_POS]
    vcf_content.loc[:,'ID'] = all_POS
    vcf_content.loc[:,'REF'] = '.'
    vcf_content.loc[:,'ALT'] = '.'
    vcf_content.loc[:,'QUAL'] = '.'
    vcf_content.loc[:,'FILTER'] = '.'
    vcf_content.loc[:,'INFO'] = '.'
    vcf_content.loc[:,'FORMAT'] = 'GP:GL'

    # round to three decimal points
    GL_RR = 10 ** lp_d_rr.astype(float)
    GL_RA = 10 ** lp_d_ra.astype(float)
    GL_AA = 10 ** lp_d_aa.astype(float)
    GL_nom = GL_RR + GL_RA + GL_AA
    GP_RR = round(GL_RR / GL_nom, 3).astype(str)
    GP_RA = round(GL_RA / GL_nom, 3).astype(str)
    GP_AA = round(GL_AA / GL_nom, 3).astype(str)
    lGL_RR = round(lp_d_rr.astype(float), 3).astype(str)
    lGL_RA = round(lp_d_ra.astype(float), 3).astype(str)
    lGL_AA = round(lp_d_aa.astype(float), 3).astype(str)

    for n in range(num):
        vcf_content.loc[:, n] = GP_RR.loc[:, n] + ',' + GP_RA.loc[:, n] + ',' + GP_AA.loc[:, n] + \
                          ':' + lGL_RR.loc[:, n] + ',' + lGL_RA.loc[:, n] + ',' + lGL_AA.loc[:, n]

    header = '##fileformat=VCFv4.2\n##fileDate=' + str(datetime.datetime.today()).split(' ')[0] + \
             '\n##source=sc_split\n##reference=hg19.fa\n##contig=<ID=1,length=249250621>\n' + \
             '##contig=<ID=10,length=135534747>\n##contig=<ID=11,length=135006516>\n##contig=<ID=12,length=133851895>\n' + \
             '##contig=<ID=13,length=115169878>\n##contig=<ID=14,length=107349540>\n##contig=<ID=15,length=102531392>\n' + \
             '##contig=<ID=16,length=90354753>\n##contig=<ID=17,length=81195210>\n##contig=<ID=18,length=78077248>\n' + \
             '##contig=<ID=19,length=59128983>\n##contig=<ID=2,length=243199373>\n##contig=<ID=20,length=63025520>\n' + \
             '##contig=<ID=21,length=48129895>\n##contig=<ID=22,length=51304566>\n##contig=<ID=3,length=198022430>\n' + \
             '##contig=<ID=4,length=191154276>\n##contig=<ID=5,length=180915260>\n##contig=<ID=6,length=171115067>\n' + \
             '##contig=<ID=7,length=159138663>\n##contig=<ID=8,length=146364022>\n##contig=<ID=9,length=141213431>\n' + \
             '##contig=<ID=MT,length=16569>\n##contig=<ID=X,length=155270560>\n##contig=<ID=Y,length=59373566>\n' + \
             '##FILTER=<ID=PASS,Description="All filters passed">\n##INFO=<ID=AN,Number=1,Type=Integer,Description="Total Allele Count">\n' + \
             '##INFO=<ID=AC,Number=A,Type=Integer,Description="Alternate Allele Count">\n' + \
             '##INFO=<ID=AF,Number=A,Type=Float,Description="Estimated Alternate Allele Frequency">\n' + \
             '##FORMAT=<ID=GL,Number=3,Type=Float,Description="Genotype Likelihood for RR/RA/AA">\n'

    with open('sc_split.vcf', 'w+') as myfile:
        myfile.write(header)
        vcf_content.to_csv(myfile, index=False, sep='\t', quoting=csv.QUOTE_NONE, escapechar='"')

if __name__ == '__main__':
    main()


