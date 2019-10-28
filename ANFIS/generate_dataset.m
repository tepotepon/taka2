% generate_dataset(7,4500,500,5) to generate a dataset following Richard's
% Memoir. I'm assuming a resolution of about 1[mm/pix].
function generate_dataset(Q, N_train, N_validate, noise_variance)
    %% Set Parameters

    % System params.
    fs = 100; %[Hz]

    % Foosball Table params.
    ball_r = 15; % 3[cm], ball diameter.
    width = 0.6*1000;
    len = 0.3*1.2*1000; % In [mm], only considering the rightmost 30%.

    %% Generate Data

    DS1 = []; % Quite inefficient to not define the size beforehand...
    while(size(DS1,1) < N_train)
        % Prevent indexing issues when Q is too large and not enough
        % samples are available for the shot.
        new_DS = [];
        while(isempty(new_DS))
            new_DS = run_exp(fs,Q,width,len,noise_variance);
        end
        DS1 = [DS1; new_DS];
    end
    
    DS2 = []; % Quite inefficient to not define the size beforehand...
    while(size(DS2,1) < N_validate)
        % Prevent indexing issues when Q is too large and not enough
        % samples are available for the shot.
        new_DS = [];
        while(isempty(new_DS))
            new_DS = run_exp(fs,Q,width,len,noise_variance);
        end
        DS2 = [DS2; new_DS];
    end
    
    % force shots that follow a path through the extremes of the table to
    % ensure sufficient range in all FIS input variables. No noise added!
    p = [0, width/2-ball_r]'; % [mm]
    v = [500,0]'; % [mm/s]
    DS1 = [run_exp2(fs,Q,width,len,p,v); run_exp2(fs,Q,width,len,-p,v); DS1];

    % Saturate to physically feasible values
    sat_x = len-ball_r;
    sat_y = width/2-ball_r;
    X = DS1(:,1:Q); X(X<0) = 0; X(X>sat_x) = sat_x;
    Y = DS1(:,Q+1:end); Y(Y<-sat_y) = -sat_y; Y(Y>sat_y) = sat_y;
    DS1 = [X Y];
    X = DS2(:,1:Q); X(X<0) = 0; X(X>sat_x) = sat_x;
    Y = DS2(:,Q+1:end); Y(Y<-sat_y) = -sat_y; Y(Y>sat_y) = sat_y;
    DS2 = [X Y];

    % Normalize the dataset
    DS1(:,1:Q) = DS1(:,1:Q)./sat_x;
    DS1(:,Q+1:end) = DS1(:,Q+1:end)./sat_y;
    DS2(:,1:Q) = DS2(:,1:Q)./sat_x;
    DS2(:,Q+1:end) = DS2(:,Q+1:end)./sat_y;
    
    %% Separate Data
    
    IN_Train = DS1(:,1:end-1);
    OUT_Train = DS1(:,end);
    IN_Validate = DS2(:,1:end-1);
    OUT_Validate = DS2(:,end);
    save('DataSet','IN_Train','OUT_Train','IN_Validate','OUT_Validate');
end