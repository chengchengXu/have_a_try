% orderID = traderBuy(Handle, Market, Code, Contracts, Price, PriceType, OrderTag)
% ���뿪���µ�; ����ʼ�п�ͷ�ֲ�, ����ƽ��, �����뿪��
%
% �������
% Handle: �˻���ʶ, double ֵ
% Market: �г�����, char ����
%  'SZSE': ���ڹ�Ʊ
%  'SSE': �Ϻ���Ʊ
%  'SHFE': �Ϻ��ڻ�
%  'DCE': ������Ʒ
%  'CZCE': ֣����Ʒ
%  'CFFEX': �н���
% Code: Ʒ�ִ���, char ����, �� 'IF0000'
% Contracts: �µ�����, double ֵ
% Price: �µ��۸�, double ֵ; �м۵��� 0
% PriceType: �µ��۸�����, char ����
%  'market': �м�
%  'limit': �޼�
% OrderTag: �������, char ����
%
% �������
% orderID: ������, double ֵ; ʧ�ܷ��� 0
%
% ��������
% ���ƻ��� 5 ��
% 1. �޳ֲ�, ֱ���� 5 �ֶ൥, ���ֲ� 5 �ֶ൥
% 2. ԭ�� 3 �ֿյ�, ����ƽ 3 �ֿյ�, ���� 5 �ֶ൥, ���ֲ� 5 �ֶ൥
% 3. ԭ�� 2 �ֶ൥, ֱ���� 5 �ֶ൥, ���ֲ� 2 + 5 = 7 �ֶ൥
%
% ʾ��
% HandleList(1) = {'FutureSimAcc'}; HandleList(2) = {'StockSimAcc'};
% handleList = traderGetHandleList();
% Handle = handleList(1);
% �� FutureSimAcc �˻��м����� 10 �ֹ�ָ�ڻ�����, ����������������Ϊ 'buy'
% ����ʼ�п�ͷ�ֲ�, ����Ƚ���ͷ�ֲ�ȫ��ƽ��, ������ 10 ��
% orderID = traderBuy(Handle, 'CFFEX', 'IF0000', 10, 0, 'market', 'buy');
