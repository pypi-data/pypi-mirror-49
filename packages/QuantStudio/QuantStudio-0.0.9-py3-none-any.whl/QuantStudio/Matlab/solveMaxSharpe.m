x = sdpvar(nVar,1);
OptimOptions = sdpsettings();
genYalmipConstraint;% �趨Լ������
[x,ResultInfo] = MaxSharpeSolverByYalmip(x,Objective,Constraints,OptimOptions);
yalmip('clear');