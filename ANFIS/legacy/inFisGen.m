load('DataSet3.mat');
genOpt = genfisOptions('SubtractiveClustering');
genOpt.Verbose = true;
% Reduce the default to force a higher number of tuneable params (cluster number).
genOpt.ClusterInfluenceRange = 0.62;
inFIS = genfis(IN_Train,OUT_Train,genOpt);
writeFIS(inFIS,'infis_20');