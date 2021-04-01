# -*- coding: utf-8 -*-
# 通联数据机密
# --------------------------------------------------------------------
# 通联数据股份公司版权所有 © 2013-2017
#
# 注意：本文所载所有信息均属于通联数据股份公司资产。本文所包含的知识和技术概念均属于
# 通联数据产权，并可能由中国、美国和其他国家专利或申请中的专利所覆盖，并受商业秘密或
# 版权法保护。
# 除非事先获得通联数据股份公司书面许可，严禁传播文中信息或复制本材料。
#
# DataYes CONFIDENTIAL
# --------------------------------------------------------------------
# Copyright © 2013-2016 DataYes, All Rights Reserved.
#
# NOTICE: All information contained herein is the property of DataYes
# Incorporated. The intellectual and technical concepts contained herein are
# proprietary to DataYes Incorporated, and may be covered by China, U.S. and
# Other Countries Patents, patents in process, and are protected by trade
# secret or copyright law.
# Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from DataYes.

'''
Created on 2017年4月11日

@author: jiangtao.sheng
'''
import re

EQUITY_DAILY_FIELDS = [
    'preClosePrice', 'openPrice', 'closePrice', 'highPrice', 'lowPrice','turnoverVol', 'turnoverValue',
    'adjFactor', 'chgPct', 'turnoverRate', 'negMarketValue', 'marketValue'
]

STOCK_DAILY_FQ_FIELDS = ['adjFactor']

EQUITY_MINUTE_FIELDS = [
    'openPrice', 'closePrice', 'highPrice', 'lowPrice', 'turnoverVol', 'turnoverValue', 'tradeDate'
]

STOCK_ADJ_FIELDS = [
    'preClosePrice', 'openPrice', 'closePrice', 'highPrice', 'lowPrice', 'turnoverVol', 'close', 'open',
    'high', 'low', 'preClose', 'closeIndex', 'openIndex', 'highIndex', 'lowIndex', 'preCloseIndex', 'volume'
]

FUTURES_DAILY_FIELDS = [
    'tradeDate', 'openPrice', 'highPrice', 'lowPrice', 'closePrice',
    'settlementPrice', 'openInterest', 'preSettlementPrice', 'turnoverVol',
    'openInt', 'settlePrice', 'symbol','chgPct', 'clearingDate', 'turnoverValue'
]

FUTURES_MINUTE_FIELDS = [
    'tradeDate', 'clearingDate', 'barTime', 'openPrice', 'highPrice', 'lowPrice',
    'closePrice', 'volume', 'tradeTime', 'turnoverVol', 'openInterest', 'symbol'
]

# 期货有些合约存在段时间所有合约退市的情况
FUTURES_SPECIAL = {
    'FU': {'start': '20180629', 'end': '20180715'},
    'WR': {'start': '20180901', 'end': '20181015'},
}

FUTURES_ARTIFICIAL = ['M0', 'M1', 'N0', 'N1', 'P0', 'P1', 'L0', 'L1', 'L3', 'L6']

TRADE_ESSENTIAL_FIELDS_DAILY = [
    'preClosePrice', 'openPrice', 'closePrice', 'highPrice', 'lowPrice', 'turnoverVol',
    'volume', 'preSettlementPrice', 'settlementPrice', 'openInterest', 'turnoverValue'
]

TRADE_ESSENTIAL_FIELDS_MINUTE = [
    'openPrice', 'closePrice', 'highPrice', 'lowPrice', 'turnoverVol', 'barTime', 'tradeTime'
]

HISTORY_ESSENTIAL_FIELDS_MINUTE = [
    'openPrice', 'closePrice', 'highPrice', 'lowPrice', 'turnoverVol',
    'turnoverValue', 'barTime', 'tradeTime', 'tradeDate'
]

ALIAS_DAILY_PRICE = set([
    'close', 'open', 'high', 'low', 'preClose', 'closeIndex', 'openIndex', 'highIndex',
    'lowIndex', 'preCloseIndex', 'volume', 'settlement', 'preSettlement'
])

ALIAS_MINUTE_PRICE = set([
    'close', 'open', 'high', 'low', 'closeIndex', 'openIndex', 'highIndex', 'lowIndex', 'volume'
])

EQUITY_MIN_BAR = [
    '09:30', '09:31', '09:32', '09:33', '09:34', '09:35', '09:36',
    '09:37', '09:38', '09:39', '09:40', '09:41', '09:42', '09:43',
    '09:44', '09:45', '09:46', '09:47', '09:48', '09:49', '09:50',
    '09:51', '09:52', '09:53', '09:54', '09:55', '09:56', '09:57',
    '09:58', '09:59', '10:00', '10:01', '10:02', '10:03', '10:04',
    '10:05', '10:06', '10:07', '10:08', '10:09', '10:10', '10:11',
    '10:12', '10:13', '10:14', '10:15', '10:16', '10:17', '10:18',
    '10:19', '10:20', '10:21', '10:22', '10:23', '10:24', '10:25',
    '10:26', '10:27', '10:28', '10:29', '10:30', '10:31', '10:32',
    '10:33', '10:34', '10:35', '10:36', '10:37', '10:38', '10:39',
    '10:40', '10:41', '10:42', '10:43', '10:44', '10:45', '10:46',
    '10:47', '10:48', '10:49', '10:50', '10:51', '10:52', '10:53',
    '10:54', '10:55', '10:56', '10:57', '10:58', '10:59', '11:00',
    '11:01', '11:02', '11:03', '11:04', '11:05', '11:06', '11:07',
    '11:08', '11:09', '11:10', '11:11', '11:12', '11:13', '11:14',
    '11:15', '11:16', '11:17', '11:18', '11:19', '11:20', '11:21',
    '11:22', '11:23', '11:24', '11:25', '11:26', '11:27', '11:28',
    '11:29', '11:30', '13:01', '13:02', '13:03', '13:04', '13:05',
    '13:06', '13:07', '13:08', '13:09', '13:10', '13:11', '13:12',
    '13:13', '13:14', '13:15', '13:16', '13:17', '13:18', '13:19',
    '13:20', '13:21', '13:22', '13:23', '13:24', '13:25', '13:26',
    '13:27', '13:28', '13:29', '13:30', '13:31', '13:32', '13:33',
    '13:34', '13:35', '13:36', '13:37', '13:38', '13:39', '13:40',
    '13:41', '13:42', '13:43', '13:44', '13:45', '13:46', '13:47',
    '13:48', '13:49', '13:50', '13:51', '13:52', '13:53', '13:54',
    '13:55', '13:56', '13:57', '13:58', '13:59', '14:00', '14:01',
    '14:02', '14:03', '14:04', '14:05', '14:06', '14:07', '14:08',
    '14:09', '14:10', '14:11', '14:12', '14:13', '14:14', '14:15',
    '14:16', '14:17', '14:18', '14:19', '14:20', '14:21', '14:22',
    '14:23', '14:24', '14:25', '14:26', '14:27', '14:28', '14:29',
    '14:30', '14:31', '14:32', '14:33', '14:34', '14:35', '14:36',
    '14:37', '14:38', '14:39', '14:40', '14:41', '14:42', '14:43',
    '14:44', '14:45', '14:46', '14:47', '14:48', '14:49', '14:50',
    '14:51', '14:52', '14:53', '14:54', '14:55', '14:56', '14:57',
    '14:58', '14:59', '15:00'
]
EQUITY_5MIN_BAR = [
    '09:30', '09:35', '09:40', '09:45', '09:50', '09:55',
    '10:00', '10:05', '10:10', '10:15', '10:20', '10:25',
    '10:30', '10:35', '10:40', '10:45', '10:50', '10:55',
    '11:00', '11:05', '11:10', '11:15', '11:20', '11:25',
    '11:30', '13:05', '13:10', '13:15', '13:20', '13:25',
    '13:30', '13:35', '13:40', '13:45', '13:50', '13:55',
    '14:00', '14:05', '14:10', '14:15', '14:20', '14:25',
    '14:30', '14:35', '14:40', '14:45', '14:50', '14:55',
    '15:00'
]
EQUITY_15MIN_BAR = [
    '09:30', '09:45', '10:00', '10:15', '10:30', '10:45', '11:00', '11:15', '11:30',
    '13:15', '13:30', '13:45', '14:00', '14:15', '14:30', '14:45', '15:00'
]

EQUITY_30MIN_BAR = ['09:30', '10:00', '10:30', '11:00', '11:30', '13:30', '14:00', '14:30', '15:00']

EQUITY_60MIN_BAR = ['09:30', '10:30', '11:30', '14:00', '15:00']

FS_FIELD = [
    'AFCOF',
    'reinsur',
    'NotesPayable',
    'refundDepos',
    'retainedEarnings',
    'NCLWithin1Y',
    'advanceReceipts',
    'policyDivPayt',
    'ACEI',
    'compensPayout',
    'AOCOF',
    'cashCEquiv',
    'AEEffectPCI',
    'NChangeInCash',
    'finanLeaseReceiv',
    'premEarned',
    'operateProfit',
    'ANICF',
    'NTrustIncome',
    'COutfFrInvestA',
    'reinsIncome',
    'TLiab',
    'purFixAssetsOth',
    'minorityInt',
    'deferRevenue',
    'estimatedLiab',
    'AOC',
    'CFrBorr',
    'NDeposDecrFrFI',
    'specOCOF',
    'depos',
    'producBiolAssets',
    'NCAA',
    'bondPayable',
    'NCompensPayout',
    'NCAE',
    'NIncrDeposInFI',
    'fValueChgGain',
    'AOR',
    'revenue',
    'assetsHeldForSale',
    'NCAWithin1Y',
    'ACE',
    'CPaidForDebts',
    'insurLiabReserRefu',
    'comprIncAttrP',
    'CInfFrOperateA',
    'fundsSecTradAgen',
    'specialReser',
    'othEffectCI',
    'LTPayable',
    'bizTaxSurchg',
    'NCApIncrRepur',
    'specificPayables',
    'derivAssets',
    'finanExp',
    'NCEBegBal',
    'NIncrBorrFrCB',
    'NIncomeBMA',
    'othLiab',
    'intanAssets',
    'reserUnePrem',
    'loanToOthBankFi',
    'specOCIF',
    'availForSaleFa',
    'othAssets',
    'CBBorr',
    'NDecrInDisburOfLa',
    'oilAndGasAssets',
    'fixedAssets',
    'purResaleFa',
    'RRReinsLinsLiab',
    'AJInvestIncome',
    'CPaidGS',
    'refundCapDepos',
    'forexEffects',
    'subrogRecoReceiv',
    'othOperCosts',
    'reinsurExp',
    'NIncomeAttrP',
    'TCL',
    'tradingFA',
    'soldForRepurFa',
    'TProfit',
    'tradingFL',
    'inventories',
    'deposFrOthBfi',
    'othPayable',
    'taxesPayable',
    'indemAccPayable',
    'refundOfTax',
    'mergedFlag',
    'premReceivAdva',
    'TLiabEquity',
    'loanFrOthBankFi',
    'secShortName',
    'CPaidInvest',
    'othCompreIncome',
    'CPaidOthInvestA',
    'specOR',
    'forexDiffer',
    'NIncrPledgeLoan',
    'dilutedEPS',
    'CPaidIFC',
    'PHInvest',
    'reinsurReceiv',
    'actPubtime',
    'TNCA',
    'endDate',
    'accruedExp',
    'othComprIncome',
    'RRReinsUnePrem',
    'ANFCF',
    'AEEffectNP',
    'othEffectSE',
    'currencyCD',
    'othEffectSA',
    'AICIF',
    'forexGain',
    'incomeTax',
    'TAssets',
    'reserInsurLiab',
    'CPaidForOthOpA',
    'TComprIncome',
    'adminExp',
    'STBorr',
    'intIncome',
    'htmInvest',
    'LTPayrollPayable',
    'NCADisploss',
    'commisPayable',
    'disburLA',
    'NotesReceiv',
    'genlAdminExp',
    'reportType',
    'dispFixAssetsOth',
    'liabHeldForSale',
    'CFrOthFinanA',
    'LTEquityInvest',
    'NoperateExp',
    'LEA',
    'gainInvest',
    'LTReceive',
    'premRefund',
    'TCA',
    'deferTaxAssets',
    'perpetualBondL',
    'compensPayoutRefu',
    'premFrOrigContr',
    'othEffectCEI',
    'perpetualBondE',
    'PHPledgeLoans',
    'COGS',
    'fixedAssetsDisp',
    'specICOF',
    'NIncBorrOthFI',
    'TCogs',
    'NReinsurPrem',
    'RD',
    'commisIncome',
    'preciMetals',
    'deferTaxLiab',
    'specFCIF',
    'othEffectCE',
    'insurReser',
    'investRealEstate',
    'specTOC',
    'othEffectTP',
    'treasuryShare',
    'settProv',
    'tRevenue',
    'indepAccAssets',
    'transacSeatFee',
    'NIncPhDeposInv',
    'CFrSaleGS',
    'endDateRep',
    'NDecrLoanToOthFI',
    'assetsImpairLoss',
    'CFrMinoSSubs',
    'specTOR',
    'NIncDispFaFS',
    'exchangeCD',
    'othCA',
    'clientProv',
    'NIncome',
    'othCL',
    'reinsurPayable',
    'NCFOperateA',
    'divReceiv',
    'othEffectNPP',
    'SEE',
    'policyDivPayable',
    'ATOR',
    'NCommisIncome',
    'SEA',
    'specFCOF',
    'sellExp',
    'deposInOthBfi',
    'othOperRev',
    'CPaidOthFinanA',
    'aeEffectOp',
    'divProfSubsMinoS',
    'NCPaidAcquis',
    'divPayable',
    'AOCIF',
    'othEffectPCI',
    'CLA',
    'NIntIncome',
    'NDecrInDeposInFI',
    'CPaidPolDiv',
    'payrollPayable',
    'origContrCIndem',
    'IFCCashIncr',
    'premiumReceiv',
    'NSecTaIncome',
    'basicEPS',
    'investAsReceiv',
    'ordinRiskReser',
    'fiscalPeriod',
    'ATOC',
    'preferredStockE',
    'NIncDispTradFA',
    'NoperateIncome',
    'LEE',
    'reserLinsLiab',
    'goodwill',
    'preferredStockL',
    'TNCL',
    'RRReinsOutstdCla',
    'specOC',
    'constMaterials',
    'AFCIF',
    'othNCA',
    'CFrOthInvestA',
    'RRReinsLThinsLiab',
    'othEquityInstr',
    'procSellInvest',
    'NDeposIncrCFI',
    'NDecrBorrFrOthFI',
    'NDispSubsOthBizC',
    'minorityGain',
    'CFrCapContr',
    'comprIncAttrMS',
    'NUndwrtSecIncome',
    'paidInCapital',
    'secID',
    'CIP',
    'clientDepos',
    'TEquityAttrP',
    'intExp',
    'reserInsurContr',
    'CAA',
    'accoutingStandards',
    'NCEEndBal',
    'CAE',
    'COutfFrFinanA',
    'investIncome',
    'LE',
    'pledgeBorr',
    'AEEffectTP',
    'intPayable',
    'NIncrLoansToOthFi',
    'NCFFrFinanA',
    'CInfFrFinanA',
    'reinsurReserReceiv',
    'othEffectOP',
    'commisExp',
    'reserLthinsLiab',
    'othNCL',
    'grossPremWrit',
    'CLE',
    'NDecrBorrFrCB',
    'LTAmorExp',
    'intReceiv',
    'CInfFrInvestA',
    'AEEffectNPP',
    'CReserCB',
    'CFrOthOperateA',
    'AA',
    'unePremReser',
    'AICOF',
    'AE',
    'prepayment',
    'transacRiskReser',
    'CPaidDivProfInt',
    'fundsSecUndwAgen',
    'AP',
    'othReceiv',
    'AR',
    'publishDate',
    'CFrIssueBond',
    'indeptAccLiab',
    'fixedTermDepos',
    'COutfOperateA',
    'ticker',
    'CPaidForTaxes',
    'NCLA',
    'reinsCostRefund',
    'capitalReser',
    'NCLE',
    'derivLiab',
    'LTBorr',
    'LA',
    'NIncFrBorr',
    'TShEquity',
    'ANOCF',
    'partyID',
    'surplusReser',
    'othEffectNP',
    'specICIF',
    'NIncDisburOfLA',
    'AEEffectCI',
    'reserOutstdClaims',
    'NCFFrInvestA',
    'CPaidToForEmpl'
]

FS_FIELD.extend([
    'TAssets_TTM',
    'TProfit_TTM',
    'forexEffects_TTM',
    'NCEEndBal_TTM',
    'basicEPS_TTM',
    'CInfFrOperateA_TTM',
    'TCL_TTM',
    'CInfFrInvestA_TTM',
    'CInfFrFinanA_TTM',
    'TLiab_TTM',
    'COutfFrInvestA_TTM',
    'othComprIncome_TTM',
    'tRevenue_TTM',
    'TCogs_TTM',
    'COutfOperateA_TTM',
    'TComprIncome_TTM',
    'COutfFrFinanA_TTM',
    'NCFOperateA_TTM',
    'NCFFrInvestA_TTM',
    'TShEquity_TTM',
    'TNCL_TTM',
    'NCFFrFinanA_TTM',
    'TNCA_TTM',
    'TCA_TTM',
    'NIncome_TTM',
    'NChangeInCash_TTM',
    'TLiabEquity_TTM',
    'operateProfit_TTM'
])

INDICE_ID_MAP = {
    'SH50': {'secID': '000016.ZICN', 'name': u'上交所：上证50'},
    'SH180': {'secID': '000010.ZICN', 'name': u'上交所：上证180'},
    'HS300': {'secID': '000300.ZICN', 'name': u'上交所：沪深300'},
    'ZZ500': {'secID': '000905.ZICN', 'name': u'上交所：中证500'}
}

STATIC_SYMBOL_MAP = {'A': u'全A股', 'ZXB': u'中小板', 'CYB': u'创业板'}

PERIOD_TYPE_LIST = ['week_first', 'week_last', 'month_first', 'month_last']

# 合约预先类型判断的pattern及list
SYMBOL_PATTERN_STOCK = '[036]\d{5}\.(XSHE|XSHG)'
SYMBOL_PATTERN_BASE_FUTURES = '[A-Z]{1,2}\d{3,4}'
SYMBOL_PATTERN_ARTIFICIAL_FUTURES = '[A-Z]{1,2}(M0|M1|N0|N1|P0|P1|L0|L1|L3|L6)'
SYMBOL_PATTERN_INDEX = '\d{6}\.ZICN'  # todo: to expand index not end with ZICN
# todo: to expand fund end with OFCN
SYMBOL_PATTERN_FUND = '[15]\d{5}\.(XSHE|XSHG)'
STOCK_PATTERN = re.compile(SYMBOL_PATTERN_STOCK)
BASE_FUTURES_PATTERN = re.compile(SYMBOL_PATTERN_BASE_FUTURES)
ARTIFICIAL_FUTURES_PATTERN = re.compile(SYMBOL_PATTERN_ARTIFICIAL_FUTURES)
INDEX_PATTERN = re.compile(SYMBOL_PATTERN_INDEX)
FUND_PATTERN = re.compile(SYMBOL_PATTERN_FUND)
XZCE_FUTURES_PATTERN = re.compile('([A-Z]{1,2})(\d{3})')
