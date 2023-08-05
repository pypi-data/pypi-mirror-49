if isfield(Objective,'X')
    Sigma = Objective.X*Objective.F*Objective.X'+diag(Objective.Delta);
else
    Sigma = Objective.Sigma;
end
% ��������Ĺ�ģʹ�ò�ͬ���㷨
if nVar>=1e3% ��ģ�ϴ�, �任����
    [x,ResultInfo] = RiskBudgetSolverByYalmip(nVar,Sigma,Objective.b);
    if ResultInfo.Status==0
        [x,ResultInfo] = RiskBudgetSolverByFmincon(nVar,Sigma,Objective.b);
    end
else% ��ģ��С���߱任��������ʧ��, ֱ�����
    [x,ResultInfo] = RiskBudgetSolverByFmincon(nVar,Sigma,Objective.b);
    if ResultInfo.Status==0
        [x,ResultInfo] = RiskBudgetSolverByYalmip(nVar,Sigma,Objective.b);
    end
end