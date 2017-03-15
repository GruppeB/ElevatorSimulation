

number_of_files = 28
seconds_in_day = 3600*24


for i in range(number_of_files):
    filename = 'double/day{}.txt'.format(i)
    with open(filename, 'r') as file:
        for line in file:
            row = line.split()
            print(float(row[0]) + i * seconds_in_day,'\t',row[1],'\t',row[2])
