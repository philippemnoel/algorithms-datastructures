%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Philippe M. Noël
% Clustering Using REpresentatives (CURE) Algorithm -- Matlab
% Original Code from Harvard APMTH120
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% loading & preparing data
X = X; % must load data from .mat file by double-clicking on it 
N = length(X(1,:));
rng(3989); % randomly shuffling data
X = X(:,randperm(N));

%% clustering N representatives using Hierarchical Clustering
N_reps = 300;
X_reps = X(:,1:N_reps);
Y = pdist(X_reps','euclid'); % distances
Z = linkage(Y,'single');
k = 2; % 2 clusters
IDX_reps = cluster(Z,'maxclust',k)

%% cluster all points by going over full dataset
for i = 1:N
  % find nearest representative to data point i
  for j = 1:N_reps
    distances(j) = norm(X(:,i) - X_reps(:,j));
  end
  % assign data point i to cluster of nearest representative point
  [M,nearest] = min(distances);
  IDX(i) = IDX_reps(nearest);
end

%% plot representatives
set(0,'defaulttextfontsize',18); set(0,'defaultaxesfontsize',18);
figure(1); clf
red_rep = X_reps(:,IDX_reps == 1); plot(red_rep(1,:),red_rep(2,:),'.r');
hold on
blue_rep = X_reps(:,IDX_reps == 2); plot(blue_rep(1,:),blue_rep(2,:),'.b');
title(sprintf('Representatives, N = %d', N_reps));
legend('Cluster #1','Cluster #2');


%% plot clustered data
figure(2); clf
red = X(:,IDX == 1); blue = X(:,IDX == 2);
plot(red(1,:),red(2,:),'.r');
hold on
plot(blue(1,:),blue(2,:),'.b');
title(sprintf('Full Data, N = %d',N));
legend('Cluster #1','Cluster #2');
