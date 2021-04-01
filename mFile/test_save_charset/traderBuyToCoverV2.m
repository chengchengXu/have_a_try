% ### traderBuyToCoverV2
% 
% 
% - ����˵��:���ڲ��Խṹ�У��յ���ƽ���µ���������ƽ���µ���
% 
% 
% - �﷨:
% 
% 	`traderBuyToCoverV2(HandleIdx,TargetIdx,Contracts,Price,PriceType,OrderTag)`
% 
% 
% - �������:
% 
% |�ֶ���	|����	|˵��
% |:-:|:-:|:-:|
% |HandleIdx	|����|�˻�����������к�
% |TargetIdx	|����|���ױ���������к�
% |Contracts	|����Ϊ�����������	|�µ�����
% |Price	|double	|�۸��м۵��۸�Ϊ0
% |PriceType	|char	|�µ��۸����� 'market': �м� 'limit': �޼�
% |OrderTag	|char	|������ǣ��û������Զ���
% 
% 
% - �������:
% 
% |�ֶ���	|����	|˵��
% |:-:|:-:|:-:|
% |orderID	|����	|ί�м�¼�ţ���������������б��
% 
% 
% - ��������:
% 
% ���ƻ���ƽ5�֣�
% 
% 1.�޳ֲ֣��˴���ƽ��Ч������޳ֲ� 
% 
% 2.ԭ��2�ֶ൥,�˴���ƽ��Ч,ά����ƽǰ��һ��״̬,���ֲ���:2�ֶ൥
% 
% 3.����7�ֿյ����ƻ���ƽ5�ֺ��˺����ֲ�Ϊ:max(7-5,0)=2����Ҫô����7-5=2�ֿյ���Ҫô�޳ֲ�
% 
% 
% ----------
% 
% - ����:
% 
% �����Ժ���
% 
%     function matlab_example_test(bInit,bDayBegin,cellPar)%
% 	    global idexD;
% 	    % ������������ʽ�̶�  
% 	    if bInit % �ж��Ƿ���Կ�������  
% 		    % ����ע�ᣬ15���ӵ�K�ߺ�5���ӵ�K��  
% 		    idexD=traderRegKData('min',15);
%         else
%             % ��õ�һ���˻���������Ϊ1�ı���ʲ��ĳֲ�
%             [Position, Frozen, AvgPrice] = traderGetAccountPositionV2(1, 1);
%             % ��û�гֲ�
%             if Position==0
%                 % ��'FutureBackReplay'�˻������м�����1��rb������Լ����������������Ϊ��sell��
%                 orderID = traderShortSellV2(1, 1, 1, 0, 'market', 'sell');
%             else
%                 % ��'FutureBackReplay'�˻������м�����ƽ��1��rb������Լ����������������Ϊ��buy��
%                 SellOrderID=traderBuyToCoverV2(1, 1, 1, 0, 'market', 'buy');
%             end        
% 	    end
%     end
% 
% ִ�нű���
% 
%     clear all;
%     clc;
%     % �趨�ز��˻�
%     AccountList(1) = {'FutureBackReplay'};
%     % �趨
%     TargetList(1).Market = 'SHFE';
%     TargetList(1).Code = 'RB0000'; % ���Ƹ���������
%     % �趨��ʼ�ʽ�ͷ��ʣ������  
%     traderSetBacktest(1000000, 0.000026,0.02,0);
%     % ����15���ӵ�Ƶ�����лز�  
%     traderRunBacktestV2('matlab_example_test',@matlab_example_test, {},AccountList,TargetList,'min',15,20180102,20180103,'FWard');
% 
% - ע�⣺
% 
% 1.PriceTypeָ��Ϊ��market���Ļ���priceʹ��0
% 2.OrderID����ֹӯֹ��Ķ������٣���0��ʼ��ţ�ÿ�β�������������±��
% 
% 
% block    char ����ָ�������ƣ�����'index'������������ָ����'plate_industry'��������ȫ����ҵ