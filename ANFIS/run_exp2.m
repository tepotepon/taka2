function DS = run_exp2(f,Q,w,l,p,v)
    
    % Ball Parameters
    ball_r = 15; % 3[cm], ball diameter.
    v_max = 5*1000; % Max and Min speeds in [mm/s].
    v_min = 0.1*1000;

    % Position and Velocity constraints:
    [theta,r] = cart2pol(v(1),v(2));
    if(theta>1)
        theta = 1;
    elseif(theta<-1)
        theta = -1;
    end
    if(r > v_max)
        r = v_max;
    elseif(r < v_min)
        r = v_min;
    end    
    [vx, vy] = pol2cart(theta,r);
    v = [vx, vy]';
    
    p(1) = 0;
    if(p(2)>w/2-ball_r)
        p(2) = w/2-ball_r;
    elseif(p(2)<-w/2+ball_r)
        p(2) = -w/2+ball_r;
    end
    
    % Simulate the shot.
    X = [p]; V = [v];
    while(1)
        s = get_state(p,v,f);
        p = s(:,1); v = s(:,2);
        if(p(1)+ball_r <= l)
            X = [X p];
            V = [V v];
        else
            % Compute the real contact point, ignoring sampling issues.
            dt_r = (l-ball_r-X(1,end))/V(1,end);
            out = X(:,end) + dt_r*V(:,end);
            break;
        end
    end
    
    % Parse the position data into the dataset format for ANFIS.
    if(length(X) >= Q)
        DS = zeros([length(X)-Q,2*Q+1]);
        for i = 1:length(X)-Q
            DS(i,:) = [X(1,i:i+Q-1), X(2,i:i+Q-1), out(2)];
        end
    else
        DS = [];
    end
end