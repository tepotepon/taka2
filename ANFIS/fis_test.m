clear, clc, close all

%% Load Training Data
load('training_data.mat');

%% Configure the FIS

genOpt = genfisOptions('SubtractiveClustering'); % Keep an eye on this.
inFIS = genfis(IN,OUT,genOpt);
opt = anfisOptions('InitialFIS',inFIS,'EpochNumber',40);

%% Train the system

fis = anfis([IN OUT],opt);
writeFIS(fis,'tacafis');

%% Validate the system

load('validation_data.mat');
test = evalfis(fis,IN);

plot(test), hold on, plot(OUT);