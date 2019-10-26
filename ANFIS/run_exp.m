function DS = run_exp(f,Q,w,l)
    
    % Ball Parameters
    ball_r = 15; % 3[cm], ball diameter.
    v_max = 5*1000; % Max and Min speeds in [mm/s].
    v_min = 0.1*1000;

    % Initial position and speed setup:
    r = randi([v_min, v_max]); % [mm/s] -> 0.1 - 8 [m/s]
    theta = randi([-2000 2000])/2000; % [rad]
    [vx, vy] = pol2cart(theta,r);
    v = [vx, vy]';
    p = [0 randi([-w/2+ball_r w/2-ball_r])]';
    
    X = [p]; V = [v];
    while(1)
        s = get_state(p,v,f);
        p = s(:,1); v = s(:,2);
        if(p(1)+ball_r <= l)
            X = [X p];
            V = [V v];
        else
            dt_r = (l-ball_r-X(1,end))/V(1,end);
            out = X(:,end) + dt_r*V(:,end);
            break;
        end
    end
    
    % Parse the position data into the dataset format for ANFIS
    DS = zeros([length(X)-Q,2*Q+1]);
    for i = 1:length(X)-Q
        DS(i,:) = [X(1,i:i+Q-1), X(2,i:i+Q-1), out(2)];
    end
end