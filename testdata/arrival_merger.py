import sys

number_of_weeks = int(sys.argv[1])

number_of_files = number_of_weeks * 7
seconds_in_day = 3600*24


for i in range(1,number_of_files+1):
    filename = 'arrivaldata/day{}.txt'.format(i)
    with open(filename, 'r') as file:
        for line in file:
            row = line.split()
            print(float(row[0]) + i * seconds_in_day,'\t',row[1],'\t',row[2])
