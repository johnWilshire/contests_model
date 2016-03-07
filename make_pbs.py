#!/usr/bin/env python
"""
    This script is to make making multiple pbs scripts easier...
"""
import argparse
parser = argparse.ArgumentParser(description='Creates pbs files')

parser.add_argument('--email', type=str,
    help='the email address of the jobs')


parser.add_argument('--modify', type=str, default="patch_area",
    help='the parameter to be modified')

parser.add_argument('--by', type=int,
    help='the ammount to step the parameter by')

parser.add_argument('--cores', type=int, default=16,
    help='the number of cores to run for')

parser.add_argument('--walltime', type=str, default='12:00:00',
    help='the allowed time for the job to run')

parser.add_argument('--dir', type=str, default='contests_model/python',
    help='the directory in which the script lives')

parser.add_argument('--sims', type=int, nargs='+', 
    help='a list of max and mins and breaks')


args = parser.parse_args()

base =  """#!/bin/bash

#PBS -l nodes=1:ppn=%s
#PBS -l vmem=120gb
#PBS -l walltime=%s
#PBS -M %s
#PBS -m ae

cd %s
""" % (args.cores, args.walltime, args.email, args.dir)


for i in range(len(args.sims) - 1):
    lower = args.sims[i] if i == 0 else args.sims[i] + args.by
    upper = args.sims[i + 1]

    call =  """Rscript run_sim.R "%s" %s %s %s %s"""  % (
        args.modify,
        lower,
        upper,
        args.by,
        args.cores)

    print base
    print call
    print '==============================='
    filename = '%s_%s_%s.pbs' % (lower, upper, args.by)
    print 'writing to %s' % filename
    print '==============================='
    f = open(filename, 'w')
    f.write(base)
    f.write(call)
    f.close()