binwidth = 5
bin(x,width)=width*floor(x/width)

set xlabel "Time (s)"
set ylabel "# travels"

plot 'data/waiting_times.data' using (bin($2,binwidth)):(1.0) smooth freq with boxes title "Waiting time"
replot 'data/service_times.data' using (bin($2,binwidth)):(1.0) smooth freq with boxes title "Service time"

pause -1