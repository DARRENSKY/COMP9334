% COMP9334 
% Week 4. Example on data centre machine availability 

% Aim: To compute the probability that exactly k machines are operating 

% Constants for the problem 
M = 120;        % Number of machines
MTTF = 500;     % Mean-time-to-failure in minutes
MRT = 20;       % Mean repair time in minutes

% The arrival and departure rates of the queueing problem 
lambda = 1/MTTF;   % Arrival rate of failed machines
mu = 1/MRT;        % Service rate of failed machines 

% We will use different number of staff 
% N is used to denote the number of staff 
vecN = [2 5 10];     % Number of repair staff can be 2, 5 or 10
lengthVecN = length(vecN);

% Calculate P(k) using the formula in the lecture notes 
% Method: Assume P(0)=1 and then compute P(1), P(2), ..., P(M).  
% Normalise to get probability. 
% 
% p(i,j) = Prob (i-1) machines failed when there are j staff
p = zeros(M+1,lengthVecN);   
for i = 1:lengthVecN  % index for number of staff 
    N = vecN(i); % number of staff      
    p(1,i) = 1; % Initislise P(0) = 1 
    for j = 2:M+1 % Calculate P(1) to P(M) 
        if j <= N+1
            p(j,i) = p(j-1,i)*(lambda*(M-j+2))/(mu*(j-1));
        else
            p(j,i) = p(j-1,i)*(lambda*(M-j+2))/(mu*N);
        end
    end
    % Normalise the column to get probability 
    p(:,i) = p(:,i) / sum(p(:,i));
end   

% Flip the matrix upside down to get 
% p(i,j) = Prob (i-1) machines working when there are vecN(j) staff
p = flipud(p);

% Plot the results 
Mv = 0:120;  % Number of working machines 
figure(1)
plot(Mv,p(:,1),'x-',Mv,p(:,2),'d-',Mv,p(:,3),'o-','MarkerSize',10)
legend('N = 2','N = 5','N = 10')
xlabel('Number of machines in operation [k]')
ylabel('Probability that exactly k machine works')
% print -dpng dcex1

q = flipud(cumsum(flipud(p)));
figure(2)
plot(Mv,q(:,1),'x-',Mv,q(:,2),'d-',Mv,q(:,3),'o-','MarkerSize',10)
legend('N = 2','N = 5','N = 10')
xlabel('Number of machines in operation [k]')
ylabel('Probability that at least k machines works')
% print -dpng dcex2
