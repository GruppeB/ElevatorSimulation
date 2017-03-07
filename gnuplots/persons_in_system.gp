set key autotitle columnheader
set xdata time
set format x "Day %j | %H:%M"
set xtics rotate

plot "data/waiting_persons.data" using ($1):2 with line, "data/persons_in_elevators.data" using ($1):2 with line

pause -1