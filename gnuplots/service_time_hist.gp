binwidth = 5
bin(x,width)=width*floor(x/width)
plot 'data/service_times.data' using (bin($2,binwidth)):(1.0) smooth freq with boxes title "Service time"
replot 'data/waiting_times.data' using (bin($2,binwidth)):(1.0) smooth freq with boxes title "Waiting time"

pause -1