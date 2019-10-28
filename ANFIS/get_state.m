% Both position and velocity must be 2-dimensional column vectors.
% The case where the ball exceeds the x limit is not handled.
function state = get_state(p,v,f)
    % Physical model parameters: dimmensions correspond to the
    % official foosball table size in millimeters, but
    % Iḿ only considering the rightmost 30 percent
    width = 0.6*1000;
    ball_r = 15; % 3[cm], ball diameter.
    dt = 1/f; % 100 Hz frame rate.
    yu = width/2;
    yl = -width/2;
    
    dt_r = 0;
    p_new = p+v*dt;
    % transform velocity from cartesian to polar coordinates
    [theta,r] = cart2pol(v(1),v(2));
    % if collision on upper edge
    if(p_new(2) > yu-ball_r)
        dt_r = dt-(yu-ball_r-p(2))/v(2);
        r = 0.98*r; % Consider some energy lost on the collision
        theta = -theta + randi([-1 1])*pi/180; % Consider some error on bounce angle.
    % if collision on lower edge
    elseif(p_new(2) < yl+ball_r)
        dt_r = dt-(yl+ball_r-p(2))/v(2);
        r = 0.98*r; % Consider some energy lost on the collision
        theta = -theta + randi([-1 1])*pi/180; % Consider some error on bounce angle.
    end
    [vx, vy] = pol2cart(theta,r);
    v_new = [vx, vy]';
    p = p + v*(dt-dt_r) + dt_r*v_new;
    state = [p v_new];
end