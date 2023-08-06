#!/usr/bin/env python

"""
randMAG is a script designed to split whole genomes into contigs
based on a distribution of sizes. Randomly reduce the completeness
based on given percentage, as well as simulate contamination by
introducing contigs from other simulated MAGs.

Produces table of created MAGs with % completeness, contamination,
and source genome.
"""

import argparse
import sys
import re
import os
import random
import string
import multiprocessing as mp
import numpy as np
from Bio import SeqIO
from scipy import stats
try:
    from randmag import FitDist
except ImportError:
    from fitdist import FitDist

BUILTIN_LENGTHS = {'Tara_bact': 'share/Tara_bact.list'}
PATH = os.path.abspath(os.path.dirname(__file__))

def _worker(seq, dist_param, min_length=300):
    basename = os.path.basename(seq)
    name = '.'.join(basename.split('.')[:-1])
    print(name)
    # find full length of genome
    genome, _ = get_seq_length(seq)
    # split into contig given sizes in loop
    all_contigs = {}
    for n, chromosome in enumerate(genome):
        contigs = {str(len(contig)) + "_" + str(n) + "_" + str(i): contig
                   for i, contig in
                   enumerate(split_contigs(chromosome, dist_param, min_length))}
        all_contigs = {**all_contigs, **contigs}
    #print(contigs)
    # return dict of genome with list of contig sizes produced
    ## to be used for contamination simulation
    #print(genome_length)
    return all_contigs, name

def get_seq_length(seq):
    """Returns a biopython SeqObject, and sequence length of given sequence
    file. Warns if file consists of multiple contigs."""
    seq_fasta = [seqi.seq for seqi in SeqIO.parse(seq, "fasta")]
    if len(seq_fasta) > 1:
        seq_fasta = check_chromosome(seq_fasta)
    # only takes the length of first contig, should be chromosome
    seq_length = len(seq_fasta[0])
    #print(type(seq_fasta[0]))
    #print(seq_fasta[0][0:20])
    return seq_fasta, seq_length

def check_chromosome(seq_fasta, cutoff=0.1):
    """Implicitly determine chromosome by % length of total sequence"""
    chromosomes = []
    all_lengths = sum([len(seq) for seq in seq_fasta])
    for seq in seq_fasta:
        if len(seq) / all_lengths > cutoff:
            chromosomes.append(seq)
    return chromosomes

def split_contigs(seq, params, min_length=300):
    """Splits given biopython SeqObject randomly according to parameters
    of a gamma distribution"""
    # get the parameters here
    shape, _, scale = params
    while seq:
        size = round(np.random.gamma(shape, scale))
        #print(size)
        contig = seq[0:size-1]
        seq = seq[size-1:]
        if len(seq) < min_length:
            contig = contig + seq
            seq = ''
        yield contig

def alter_completeness(contigs, completeness):
    """Given a set of contigs in a dict, randomly removes one contig at
    a time until desired completeness is reached, or below."""
    # get the dict keys of contig lengths
    contig_lengths = {length: int(''.join(length.split('_')[0])) for length in contigs.keys()}
    contig_keys = [key for key in contigs.keys()]
    # sum for complete genome length
    total_length = sum(contig_lengths.values())
    # try to remove contig lengths down to completeness
    removed_contigs = []
    removed_sizes = []
    while sum(removed_sizes) < (1 - float(completeness)) * total_length:
        removed_contigs.append(random.choice(list(contig_keys)))
        contig_keys = [key for key in contig_keys if not key in removed_contigs]
        #print(removed_contigs)
        # relies on key name being "ID_len"
        removed_sizes.append(int(removed_contigs[-1].split('_')[0]))
    new_contigs = {contig: contigs[contig] for contig in
                   contig_lengths.keys() if contig not in removed_contigs}
    new_completeness = 1 - sum(removed_sizes) / total_length
    return new_contigs, new_completeness

def add_contamination(genome, all_contigs, contamination=1.0):
    """Adds random contigs to a simulated MAG from other simulated MAGS,
    to simulate contamination to specified fraction."""
    contig_lengths = {length: int(''.join(length.split('_')[0])) for length
                      in genome.keys()}
    # sum for complete genome length
    total_length = sum(contig_lengths.values())
    i = 0
    new_contamination = 1.0
    total_contam_size = 0
    used_sets = []
    # check if contaminated enough else loop
    while contamination > new_contamination:
        # random sample a genome from list of genomes
        rand_genome = random.choice(all_contigs)
        ## random sample a contig within genome
        genome["c" + str(i)] = random.choice(list(rand_genome.values()))
        contam_size = len(genome["c" + str(i)])
        if (rand_genome, contam_size) in used_sets:
            continue
        used_sets.append((rand_genome, contam_size))
        total_contam_size = total_contam_size + contam_size
        new_contamination = (total_length + total_contam_size) / total_length
        i += 1
    return genome, new_contamination

def output_randcontigs(name, genome, completeness, contamination, q):
    """Writes shuffled contigs to file"""
    # give randomised names to avoid writing same file
    randname = ''.join([random.choice(string.ascii_lowercase)
                        for _ in range(8)])
    q.put((name, randname, completeness, contamination))
    with open(name + '_' + randname + ".fna", "w") as handle:
        # necessary to put keys into list before shuffle
        shuffled_headers = list(genome.keys())
        random.shuffle(shuffled_headers)
        #all_c = sum([len(seq) for seq in genome.values()])
        #print(all_c)
        for header in shuffled_headers:
            handle.write(">" + str(header) + "\n")
            handle.write(str(genome[header]) + "\n")

def _listener(q):
    with open("simulated_MAGs.tab", "w") as handle:
        while True:
            out = q.get()
            if out == "done":
                break
            for each in out:
                handle.write(str(each) + '\t')
            handle.write('\n')

def main():
    parser = argparse.ArgumentParser(description="""
                                    Simulate MAGs by splitting whole
                                    genomes."""
                                     )
    parser.add_argument("genome_tab", help="Genomes in .fna in list format")
    parser.add_argument("distribution", help="Set of lengths to base the "
                                             "distribution on.")
    parser.add_argument("-c", "--completeness", default="1.0",
                        help="Range of completeness levels to be produced. "
                             "Default=1.0")
    parser.add_argument("-r", "--contamination", default=1.0, type=float,
                        help="Range of contamination to be included in "
                             "produced MAGs. Default=0.0")
    parser.add_argument("-n", "--num", default=False, type=int,
                        help="Number of randomised MAGs to produce. Produces "
                             "one randomised per provided genome by default.")
    args = parser.parse_args()

    if args.distribution in BUILTIN_LENGTHS.keys():
        args.distribution = os.path.join(PATH, BUILTIN_LENGTHS[args.distribution])
    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(processes=2)
    listener = pool.apply_async(_listener, (q,))
    with open(args.genome_tab) as seq_file:
        input_seqs = [seq.strip() for seq in seq_file
                      if not re.match('#|\n', seq)]

    with open(args.distribution) as dist_file:
        distances = [int(dist.strip()) for dist in dist_file
                     if not re.match('#|\n', dist)]
    # here get distribution and parameters
    f = FitDist(distances)
    # finding best distribution for the data
    # mostly pointless since this script presumes that is gamma
    distribution = f.find_best_dist()
    f.histogram(distribution)
    params = stats.gamma.fit(distances)

    if not args.num:
        args.num = len(input_seqs)
    all_mags = []
    while args.num > 0:
        for seq in input_seqs:
            while True:
                contigs, name = _worker(seq, params, min(distances))
                contigs, completeness = alter_completeness(contigs,
                                                           args.completeness)
                # if empty due to low completeness request - retry
                if not contigs or float(args.completeness) - completeness > 0.05:
                    continue
                break
            all_mags.append((name, completeness, contigs))
            args.num -= 1
            #print(args.num)
            if args.num <= 0:
                break
    raw_mags = [mag[2] for mag in all_mags]
    for name, completeness, mag in all_mags:
        contam_mag, contamination = add_contamination(mag, raw_mags,
                                                      args.contamination)
        output_randcontigs(name, contam_mag, completeness, contamination, q)
    q.put("done")
    listener.get()
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()
