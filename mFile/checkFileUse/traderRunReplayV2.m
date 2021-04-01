% traderRunReplayV2(StrategyName, TradeFun, varFunParameter, AccountList, TargetList, KFrequency, KFreNum, BeginDate, RepalyDate, FQ, AlgoTradeFun, varAlgoFunParameter)
% ʵ�ֲ��ԵĻط�
%
% �������
% StrategyName: ��������, char ����
% TradeFun: ���Ժ���, function_handle ��, ��ʽ: @��������
% varFunParameter: ���Ժ������õ��Ĳ���, cell ����, �� {'����һ', '������', '������'}
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
% RepalyDate: ���Իطŵ�����, double ��, �� 20140610, Ҫ�� BeginDate <= RepalyDate
% FQ: ��Ȩ����, char ����
%  'NA': ����Ȩ
%  'FWard': ��ǰ��Ȩ
%  'BWard': ���Ȩ
% AlgoTradeFun: �㷨���׺���, function_handle ��, ��ʽ: @�㷨���׺���
% varAlgoFunParameter: �㷨���׺������õ��Ĳ���, cell ����
%
% ʾ��
% �Բ��� Strategy �ط�, �ط�����Ϊ 2015 �� 5 �� 25 ��, ���Կ�ʼʱ��Ϊ 2015 �� 5 �� 20 ��
% AccountList(1) = {'FutureBackReplay'};
% TargetList(1).Market = 'CFFEX'; TargetList(1).Code = 'IF0000';
% TargetList(2).Market = 'CFFEX'; TargetList(2).Code = 'IH0000';
% traderRunReplayV2('Strategy', @Strategy, {len1, len2, stopTar, profitTar, pct, shareNum}, AccountList, targetList, 'min', 1, 20150520, 20150525, 'FWard');
%
% �Բ��� Strategy �ط�, �ط�����Ϊ 2015 �� 5 �� 25 ��, ���Կ�ʼʱ��Ϊ 2015 �� 5 �� 20 ��
% AccountList(1) = {'StockBackReplay'};
% TargetList(1).Market = 'SZSE'; TargetList(1).Code = '000002';
% TargetList(2).Market = 'SZSE'; TargetList(2).Code = '000001';
% traderRunReplayV2('Strategy', @Strategy, {len1, len2, stopTar, profitTar, pct, shareNum}, AccountList, targetList, 'min', 1, 20150520, 20150525, 'FWard');