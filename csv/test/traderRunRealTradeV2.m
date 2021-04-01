% traderRunRealTradeV2(StrategyName, TradeFun, varFunParameter, AccountList, TargetList, KFrequency, KFreNum, BeginDate, FQ, AlgoTradeFun, varAlgoFunParameter)
% ʵ�ֲ��Ե�ʵ�̽���
%
% �������
% StrategyName: ��������, char ����
% TradeFun: ���Ժ���, function_handle ��, ��ʽ: @��������
% varFunParameter: ���Ժ������õ��Ĳ���, cell ����
% AccountList: �˻�����, cell ����
% TargetList: ���Ա���б�, struct ����
%  Market: �г�����, char ����
%  Code: Ʒ�ִ���, char ����, �� '000002'
% KFrequency: ����ˢ��Ƶ������, char ����
%  'tick': tick Ƶ
%  'min': ����Ƶ
%  'day': ��Ƶ
% KFreNum: ˢ��Ƶ����ֵ, double ��
% BeginDate: ���Կ�ʼ������, double ��, �� 20140608
% FQ: ��Ȩ����, char ����
%  'NA': ����Ȩ
%  'FWard': ��ǰ��Ȩ
%  'BWard': ���Ȩ
% AlgoTradeFun: �㷨���׺���, function_handle ��, ��ʽ: @�㷨���׺���
% varAlgoFunParameter: �㷨���׺������õ��Ĳ���, cell ����
%
% ʾ��
% �Բ��� Strategy ʵʱ����, ���Բ���Ϊ {len, plus, ShareNum}, ȡ���ݵĿ�ʼʱ��Ϊ 2015 �� 1 �� 1 ��
% AccountList(1) = 'FutureSimAcc';
% TargetList(1).Market = 'CFFEX'; TargetList(1).Code = 'IF0000';
% TargetList(2).Market = 'CFFEX'; TargetList(2).Code = 'IH0000';
% traderRunRealTradeV2('Strategy', @Strategy, {len, plus, ShareNum}, AccountList, TargetList, 'min', 1, 20150101, 'FQ');