function train_tacafis(dataset, clust, initStep, decRate, incRate, ID)
    % Graphics Settings
    set(groot, 'defaultFigureUnits','normalized');
    set(groot, 'defaultFigurePosition',[0 0 1 1]);

    % String stuff handling
    sess_name = strcat("Session_",string(ID));
    infis_name = strcat("infis_",string(clust));
    sgt = strcat("CN = ",string(clust), ", IS = ", string(initStep),...
        ", DR = ", string(decRate), ", IR = ", string(incRate));
    
    % Load Data and initial FIS.
    load(dataset, 'IN_Train', 'IN_Validate', 'OUT_Train', 'OUT_Validate');
    inFIS = readfis(infis_name);

    % Configure Optimization Parameters
    opt = anfisOptions;
    opt.InitialFIS = inFIS;
    opt.EpochNumber = 100;
    opt.InitialStepSize = initStep;
    opt.StepSizeDecreaseRate = decRate;
    opt.StepSizeIncreaseRate = incRate;
    opt.DisplayANFISInformation = 0;
    opt.DisplayErrorValues = 0;
    opt.DisplayStepSize = 0;
    opt.DisplayFinalResults = 0;
    opt.ValidationData = [IN_Validate OUT_Validate];

    % Train the system
    [fis,trnErr,stepSize,chkFIS,chkErr] = anfis([IN_Train OUT_Train],opt);
    save(sess_name,'chkErr', 'stepSize', 'trnErr', 'chkFIS', 'fis');
    test_fis1 = evalfis(fis,IN_Validate);
    test_fis2 = evalfis(chkFIS,IN_Validate);

    % Plot and Store Training Results
    f = figure('visible','off'); x = 1:length(trnErr);    
    subplot(3,2,1), plot(stepSize), title('Step Size');    
    subplot(3,2,2), plot(x,trnErr,'.b',x,chkErr,'*r');
    legend('Training Error', 'Check Error'), title('Error');
    subplot(3,2,[3 4]),plot(test_fis1), hold on, plot(OUT_Validate);
    legend('Train FIS Output', 'Sim Output');
    subplot(3,2,[5 6]),plot(test_fis2), hold on, plot(OUT_Validate);
    legend('Check FIS Output', 'Sim Output');
    sgtitle(sgt); saveas(f,sess_name,'fig'); saveas(f,sess_name,'png');
end