%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Philippe M. Noël
% PageRank Algorithm -- Matlab
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% data
alpha = 0.9; N = 6;
Q = [1/6,1/6,1/6,1/6,1/6,1/6;
     1/2,  0,1/2,  0,  0,  0;
     1/3,1/3,  0,1/3,  0,  0;
       0,  0,1/3,  0,1/3,1/3;
       0,  0,  0,1/2,  0,1/2;
       0,  0,  0,  1,  0,  0];
disp('Q = '); disp(Q);

%% algorithm data processing
% fix nodes without outgoing links, if any
for i = 1:N
    if sum(Q(i,:)) == 0
        Q(i,:) = ones(1,N) * (1 / N)
    end
end
% add teleportation factor
Q = alpha * Q + (1 - alpha) * (1 / N) * ones(N)

%% get eigenvalues of Q
[V,D] = eigs(Q',1); V = abs(V)'

%% perform power-method 
x = ones(1,6) % initial guess
for i = 1:20 % we arbitrarily decide upon 20 iterations
    x = x * Q
end

%% compare convergence result with eigenvalues
x = x / norm(x) % display normalized x to compare with eigenvalues
V % not bad
