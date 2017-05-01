set key autotitle columnheader
set xdata time
set format x "Day %j | %H:%M"
set xtics rotate
set ylabel "Time (s)"

plot "data/waiting_times.data" using ($1):2 with line, "data/service_times.data" using ($1):2 with line

pause -1