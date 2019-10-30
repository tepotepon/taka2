%% Load Training and Validation Data

load('DataSet3.mat');

%% Configure and compute Initial FIS or read an existing one.

genOpt = genfisOptions('SubtractiveClustering');
genOpt.Verbose = true;
%genOpt.ClusterInfluenceRange = 0.4; % Reduce the default to force a higher number of tuneable params.
inFIS = genfis(IN_Train,OUT_Train,genOpt);
writeFIS(inFIS,'inFIS2_3');
%inFIS = readfis('inFIS2');

%% Configure the Optimization Parameters

opt = anfisOptions;
opt.InitialFIS = inFIS;
opt.EpochNumber = 60;
opt.InitialStepSize = 0.1;
opt.StepSizeDecreaseRate = 0.9;
opt.StepSizeIncreaseRate = 1.6;
opt.ValidationData = [IN_Validate OUT_Validate];

%% Train the system

[fis,trainError,stepSize,chkFIS,chkError] = anfis([IN_Train OUT_Train],opt);
writeFIS(fis,'tacafis_smallDS3');
save('SessionSDS3','chkError', 'stepSize', 'trainError')

%% Display Training Results
close all,

figure,subplot(2,2,1),plot(stepSize)
x = 1:length(trainError);
subplot(2,2,2),plot(x,trainError,'.b',x,chkError,'*r')
legend('Training Error', 'Check Error');
test = evalfis(fis,IN_Train);
subplot(2,2,[3 4]),plot(test), hold on, plot(OUT_Train);
legend('Predicted Output', 'Real Output')