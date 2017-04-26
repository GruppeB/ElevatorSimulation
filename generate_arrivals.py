import argparse
import sys
from subprocess import call

def run(args):

    NN = args.NN
    NU = args.NU
    N_weeks = args.N_weeks

    days_in_week = 7
    N_days = days_in_week * N_weeks

    print("Generating days")

    print("\r0/{}".format(N_days), end="")
    for day in range(1, N_days+1):
        call("python3 arrival_model.py {} {} cat > arrivaldata/day{}.txt".format(NN, NU, day), shell = True)
        print("\r{}/{}".format(day, N_days),end="")
    print()

    print("Generating weeks")
    print("\r0/{}".format(N_weeks), end="")

    for week in range(1, N_weeks+1):
        call("python3 arrival_merger.py {} cat > arrivaldata/week{}.txt".format(week, week), shell = True)
        print("\r{}/{}".format(week, N_weeks), end="")
    print()

def main():
    parser=argparse.ArgumentParser()

    parser.add_argument("NN", type = int, help = "Antall personer trukket fra normalfordeling")
    parser.add_argument("NU", type = int, help = "Antall personer trukket fra uniformfordeling")
    parser.add_argument("N_weeks", type = int, help = "Antall uker man genererer data for")

    run(parser.parse_args())

main()
