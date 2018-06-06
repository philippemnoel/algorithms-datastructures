%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Philippe M. Noël
% Singular Value Decomposition - Maximum Covariance Analysis -- Matlab
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% data processing
Y = [1,2,3,4,5,4,3,2,1,0;
     2,3,4,5,6,5,4,3,2,1;
     6,4,6,4,6,4,6,4,6,4;
     9,5,9,5,9,5,9,5,9,5]; % 4 stocks
X = [1,2,3,4,5,4,3,2,1,0;
     9,8,7,8,9,8,7,8,9,8;
     2,3,4,5,6,5,4,3,2,1]; % 3 stocks
[M,~]=size(Y);
[L,N]=size(X);
% add noise
rng(3958);
Y = Y + 1.5 * rand(M,N);
X = X + 1.5 * rand(L,N);
% remove time mean, so we only have price anomalies
for m = 1:M
    Y(m,:) = Y(m,:) - mean(Y(m,:));
end
for l = 1:L
    X(l,:) = X(l,:) - mean(X(l,:));
end
% final processing of the data
Y(1:2,:) = Y(1:2,:) * 3;
X(2,:) = X(2,:) * 0.5;
X(3,:) = -X(3,:);

%% plotting the data
figure(1); clf
set(0,'defaulttextfontsize',18); set(0,'defaultaxesfontsize',18);
hlY = plot(1:N,Y(1,:),'-rx',1:N,Y(2,:),'-g+',1:N,Y(3,:),'-bo',1:N,Y(4,:),'-k'); hold on
hlX=plot(1:N,X(1,:),'--rx',1:N,X(2,:),'--g+',1:N,X(3,:),'--bo');
set(hlY,'linewidth',3,'markersize',12); xlabel('Day'); ylabel('Stock Prices')
title('Stock Prices: NY (thick) & Tokyo (thin)')
legend('NY1','NY2','NY3','NY4','Tokyo1','Tokyo2','Tokyo3')

%% MCA evaluation
C = Y * X' / N % covariance matrix
% SVD to find PCs & explained covariance
[U,S,V] = svd(C);
disp('Singular values are:')
disp(diag(S)');
% based on singular values, only need first mode
disp('Based on the singular values, only the first SVD mode matters')
disp('U(:,1):'); disp(U(:,1)')
disp('V(:,1):'); disp(V(:,1)')
