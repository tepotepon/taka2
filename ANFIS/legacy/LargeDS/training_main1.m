%% Load Training and Validation Data

load('DataSet1.mat');

%% Configure and compute Initial FIS or read an existing one.

%genOpt = genfisOptions('SubtractiveClustering', 'Verbose', true);
%inFIS = genfis(IN_Train,OUT_Train,genOpt);
inFIS = readfis('tacafis3');

%% Configure the Optimization Parameters

opt = anfisOptions;
opt.InitialFIS = inFIS;
opt.EpochNumber = 20;
opt.InitialStepSize = 0.0911073856;
opt.StepSizeDecreaseRate = 0.9;
opt.StepSizeIncreaseRate = 1.4;
opt.ValidationData = [IN_Validate OUT_Validate];

%% Train the system

[fis,trainError,stepSize,chkFIS,chkError] = anfis([IN_Train OUT_Train],opt);
writeFIS(fis,'tacafis4');
save('Session4','chkError', 'stepSize', 'trainError')

%% Validate the system

%test = evalfis(fis,IN_Validate);
%plot(test), hold on, plot(OUT_Validate);