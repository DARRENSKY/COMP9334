% author: Fudi Zheng
% Refer to week4's lecture
% After working out the balance equation, we need to solve
% the set of linear equations
% 
% We put the linear equations in standard form A x = b
% where x is the unknown vector  
% 
A=[ 20,-20,0,-10,0,0;
    -20,40,-10,0,0,-20;
    0,-20,50,-20,-20,0;
    0,0,-20,30,0,0;
    0,0,-20,0,30,-20;
    0,0,0,0,-10,40;
    1,1,1,1,1,1]
b=[0 0 0 0 0 0 1]';
x = A\b