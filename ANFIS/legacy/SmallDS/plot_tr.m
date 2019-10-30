clear, clc, close all;
load('DataSet2.mat');
i = 1;
while(j < length(OUT_Train))
    j = i;
    while(OUT_Train(j) == OUT_Train(i))
        j = j+1;
    end
    trayectoria_x = [];
    trayectoria_y = [];
    for k = i:j-1
        trayectoria_x = [trayectoria_x IN_Train(k,1:7)];
        trayectoria_y = [trayectoria_y IN_Train(k,8:14)];
    end
    i = j;
    plot(trayectoria_x,trayectoria_y);
end