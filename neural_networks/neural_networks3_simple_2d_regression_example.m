%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Philippe M. Noël
% Neural Network 2D Regression Algorithm -- Python 3
% Original Code from Harvard APMTH120
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% data
X = [2,7,0,7,4,3,9,1,8,4,10,6,4,5,2,3,5,8,3,4;
     10,6,7,10,8,1,3,4,4,1,1,7,10,8,0,0,2,4,6,9];
y = [3,3,1,3,3,1,2,1,2,1,2,3,3,3,1,1,2,2,1,3];
% plotting
figure(1); clf
set(0,'defaulttextfontsize',16); set(0,'defaultaxesfontsize',16);
xlim([-1,11]); xlabel('x')
ylim([-1,11]); ylabel('y'); box on
for i = 1:length(y)
  text(X(1,i), X(2,i), num2str(y(i)));
end
title('Training Data: Label as Function of (x,y)');

%% creating the neural network model & training it
rng(3456);
net = feedforwardnet([3 3]);
net.divideFcn=''; % don't divide data into training, testing, validation
net = train(net, X, y); h_net = view(net);

%% classify a new point
X_test = [4 4]';
y_pred = net(X_test);
disp('X_test = '); disp(X_test')
disp('y_pred = '); disp(y_pred')

%% terminate
nntraintool('close'); close(h_net)
