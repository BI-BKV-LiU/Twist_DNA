# vim: syntax=python tabstop=4 expandtab
# coding: utf-8

__author__ = "Patrik Smeds"
__copyright__ = "Copyright 2021, Patrik Smeds"
__email__ = "patrik.smeds@scilifelab.uu.se"
__license__ = "MIT"

import re
import argparse
import pysam

regex_string = ":UMI_([A-Za-z]+-[A-Za-z]+)"
regex = re.compile(regex_string)

parser = argparse.ArgumentParser(description="Will look for UMI_{TAG1}-{TAG2} in read name, remove it and add it as attribute.")
parser.add_argument('-i', '--input', help='input bam file', required=True)
parser.add_argument('-o', '--output', help='output bam file', required=True)
parser.add_argument('-a', '--attribute', help='attribute name', default="RX")

args = parser.parse_args()


input_bam_file = pysam.AlignmentFile(args.input, "r" if args.input.endswith(".sam") else "rb")

with pysam.AlignmentFile(args.output, "w" if args.output.endswith(".sam") else "wb", template=input_bam_file) as output_bam_file:
    for read in input_bam_file.fetch():
        umi = regex.search(read.query_name)[1]
        read.query_name = regex.sub("", read.query_name)
        read.tags += [(args.attribute, umi)]
        output_bam_file.write(read)
