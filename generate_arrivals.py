#!/usr/bin/env python3

import argparse
import sys
from subprocess import call

def run(args):

    NN = args.NN
    NU = args.NU
    N_weeks = args.N_weeks

    days_in_week = 7
    N_days = days_in_week * N_weeks

    print("\rGenerating day 0/{}".format(N_days), end="")
    for day in range(1, N_days+1):
        call("python3 environment/arrival_model.py {} {} cat > arrivaldata/day{}.txt".format(NN, NU, day), shell = True)
        print("\rGenerating day {}/{}".format(day, N_days),end="")
    print()

    print("Merging ... ", end="")
    call("python3 environment/arrival_merger.py {} cat > arrivaldata/alldays.txt".format(N_weeks), shell = True)
    print("done!")

def main():
    parser=argparse.ArgumentParser()

    parser.add_argument("NN", type = int, help = "Antall personer trukket fra normalfordeling")
    parser.add_argument("NU", type = int, help = "Antall personer trukket fra uniformfordeling")
    parser.add_argument("N_weeks", type = int, help = "Antall uker man genererer data for")

    run(parser.parse_args())

main()
