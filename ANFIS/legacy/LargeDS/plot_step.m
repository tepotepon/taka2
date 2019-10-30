load('Session1');
s = [stepSize];

load('Session2');
s = [s; stepSize];

load('Session3');
s = [s; stepSize];

load('Session4');
s = [s; stepSize];
plot(s)