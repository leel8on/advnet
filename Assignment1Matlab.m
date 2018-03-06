clear;
n = 1;
done = 0;
W = zeros(10000,1); %a raw estimator
Y = zeros(10000,1); %b control variate sum of service times
Q = zeros(10000,1); %c control variate
L = zeros(10000,1); %d reduction
Wbar = zeros(10000,1);
Zbar = zeros(10000,1);
Hbar = zeros(10000,1);
Lbar = zeros(10000,1);
Wwidth = zeros(10000,1); %raw estimator confidence interval width
Zwidth = zeros(10000,1);
Hwidth = zeros(10000,1);
Lwidth = zeros(10000,1);

stopW = 0;
stopZ = 0;
stopH = 0;
stopL = 0;

x = 1.645; %.9 confidence interval

while done ~= 1
    T = zeros(10,1); %Total time
    Queue = zeros(10,1); %Queue time
    S = zeros(10,1); %Service time
    A = zeros(10,1); %Arrival times
    Start = zeros(10,1); %Start service times
    Stop = zeros(10,1); %Stop service times
    Nframes = zeros(10,1); %num frames in queue when pkt i arrives
    %Calculate service times
    for i = 1:length(S)
        S(i) = exprnd(1);
    end
    %Run simulation
    ctime = 0; %current time
    %Set first frame values
    A(1) = 0;
    Start(1) = 0; %No queue time
    Stop(1) = S(1); %No queue time
    %Queue(1) = 0; %No queue time
    T(1) = S(1); %No queue time
    for i = 2:length(T)
        arr = exprnd(.5); %packet arrival
        A(i) = A(i-1) + arr;
        if A(i) > Stop(i-1)
            Start(i) = A(i);
        else
            Start(i) = Stop(i-1);
        end
        Stop(i) = Start(i) + S(i);
        %Queue(i) = Start(i) - A(i);
        T(i) = Stop(i) - A(i);
        
        %calculate num frames in queue
        doneFrames = 0;
        frameCounter = i;
        while doneFrames ~= 1
            if frameCounter < 2
                doneFrames = 1;
            else
                if A(i) < Stop(frameCounter - 1)
                    Nframes(i) = Nframes(i) + 1;
                else
                    doneFrames = 1;
                end
            end
            frameCounter = frameCounter - 1;
        end
    end
    
    %%%%%%%%%%%%%%% a raw estimator
    W(n) = sum(T); %Add nth sample into W array
    Wbar(n) = sum(W) / n; %calculate raw estimator
    
    %calculate Wbar interval
 
    %calculate Sn
    Sn = sqrt(var(W(1:n)));
    %RawInterval = [Wbar - (x*Sn)/sqrt(n), Wbar + (x*Sn)/sqrt(n)];
    Wwidth(n) = (2*x*Sn)/sqrt(n);
    if n > 10 && stopW == 0 && (Wwidth(n)) <= Wbar(n)*.1
        stopW = n;
    end
    
    %%%%%%%%%%%%%%
    %b control variate for the frame service times
    Y(n) = sum(S);
    Ybar = sum(Y)/n;
    
    Yvar = var(Y(1:n));
    
    %zCovar = myCovar(W, Y, Wbar, Ybar, n);
    zCovarTemp = cov(W(1:n),Y(1:n));
    zCovar = zCovarTemp(1,2);
    cZ = -zCovar/Yvar;
    Zbar(n) = Wbar(n) + cZ*(Ybar - 10);
    %calculate Zbar interval
    Sz = sqrt((Sn^2) - ((zCovar^2)/Yvar));
    Zwidth(n) = (2*x*Sz)/sqrt(n);
    
    if n > 10 && stopZ == 0 && (Zwidth(n)) <= Zbar(n)*.1
        stopZ = n;
    end
    
    %%%%%%%%%%%%%
    %c control variate
    
    %calculate Q(n)
    tempSum = 0;
    for i = 1:9
        tempSum = tempSum + A(i+1) - A(i);
    end
    Q(n) = Y(n) - tempSum;
    
    Qbar = sum(Q)/n;
    
    %calculate variance
    Qvar = var(Q(1:n));
    %calculate covariance
    %qCovar = myCovar(W, Q, Wbar, Qbar, n);
    qCovarTemp = cov(W(1:n),Q(1:n));
    qCovar = qCovarTemp(1,2);
    cQ = -qCovar/Qvar;
    Hbar(n) = Wbar(n) + cQ*(Qbar - 5.5);
    %calculate Hbar interval
    Sh = sqrt((Sn^2) - (qCovar^2)/Qvar);
    Hwidth(n) = (2*x*Sh)/sqrt(n);
    
    if n > 10 && stopH == 0 && (Hwidth(n)) <= Hbar(n)*.1
        stopH = n;
    end
    
    %%%%%%%%%%%%%
    %d reduction
    L(n) = sum(Nframes) + 10;
    Lbar(n) = sum(L)/n;
    
    %calculate Lbar interval
    Sl = sqrt(var(L(1:n)));
    Lwidth(n) = (2*x*Sl)/sqrt(n);
    
    if n > 10 && stopL == 0 && (Lwidth(n)) <= Lbar(n)*.1
        stopL = n;
    end
    
    n = n + 1; %increment n
    if n > 1000
        done = 1;
    end
end
%plot first problem
figure;
n = n-1;
x = 2:1000;
plot(x, Wbar(2:n), x, Zbar(2:n), x, Hbar(2:n), x, Lbar(2:n));
xlabel('Simulation run n');
ylabel('Estimated \theta');
title('Simulation estimates of \theta over 1000 runs from 4 estimators');
legend('W', 'Z', 'H', 'L');

figure;
plot(x, Wwidth(2:n), x, Zwidth(2:n), x, Hwidth(2:n), x, Lwidth(2:n));
xlabel('Simulation run n');
ylabel('Confidence interval width');
title('Confidence interval width of 4 estimators over 1000 runs of simulation');
legend('W', 'Z', 'H', 'L');

figure;
hold on;
x = 2:stopW;
plot(x, Wbar(2:stopW));
x = 2:stopZ;
plot(x, Zbar(2:stopZ));
x = 2:stopH;
plot(x, Hbar(2:stopH));
x = 2:stopL;
plot(x, Lbar(2:stopL));
legend('W', 'Z', 'H', 'L');
xlabel('Simulation run n');
ylabel('Confidence interval width');
title('Quickness of 4 estimators to reach interval width \pm 10% of estimated value');
text(stopW, Wbar(stopW), sprintf('Wbar: %d', stopW));
text(stopZ, Zbar(stopZ), sprintf('Zbar: %d', stopZ));
text(stopH, Hbar(stopH), sprintf('Hbar: %d', stopH));
text(stopL, Lbar(stopL), sprintf('Lbar: %d', stopL));
