function generate_dataset(Q, N_train, N_validate, noise_variance)
    %% Set Parameters

    % System params.
    fs = 100; %[Hz]
    N_trials = N_train+N_validate;

    % Foosball Table params.
    width = 0.6*1000;
    len = 0.3*1.2*1000; % In [mm], only considering the rightmost 30%.

    %% Generate Data

    DS = []; % Quite inefficient to not define the size beforehand...
    for k = 1:N_trials
        DS = [DS; run_exp(fs,Q,width,len)];
    end

    % Add noise to dataset
    DS = DS + [noise_variance*randn(size(DS(:,1:end-1))) zeros(size(DS(:,end)))];

    % Saturate to phisically feasible values
    X = DS(:,1:Q); X(X<0) = 0; X(X>len) = len;
    Y = DS(:,Q+1:end); Y(Y<-width/2) = -width/2; Y(Y>width/2) = width/2;
    DS = [X Y];

    % Normalize the dataset
    DS(:,1:Q) = DS(:,1:Q)./len;
    DS(:,Q+1:end) = DS(:,Q+1:end)./(width/2);
    
    %% Separate Data
    
    IN = DS(1:N_train,1:end-1);
    OUT = DS(1:N_train,end);
    save('training_data','IN','OUT');
    IN = DS(N_train+1:end,1:end-1);
    OUT = DS(N_train+1:end,end);
    save('validation_data','IN','OUT');
end