import json
import mpld3
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import pandas as pd
import numpy as np

def make_df_cf_waterfall(graph_대상, fs_type, years):

    if fs_type == "별도":
        df = pd.read_excel("static/dart_fs.xlsx", sheet_name='별도', header=0)
    else:
        df = pd.read_excel("static/dart_fs.xlsx", sheet_name='연결', header=0)


    names_cf = {'영업활동CF': 'ifrs-full_CashFlowsFromUsedInOperatingActivities',
                '투자활동CF': 'ifrs-full_CashFlowsFromUsedInInvestingActivities',
                '재무활동CF': 'ifrs-full_CashFlowsFromUsedInFinancingActivities',
                '기초CF': 'dart_CashAndCashEquivalentsAtBeginningOfPeriodCf',
                '기말CF': 'dart_CashAndCashEquivalentsAtEndOfPeriodCf',}


    index_cf= ["FY18말 현금","FY19_영업활동CF","FY19_투자활동CF","FY19_재무활동CF","FY19_기타CF",
             "FY19말 현금", "FY20_영업활동CF", "FY20_투자활동CF", "FY20_재무활동CF", "FY20_기타CF",
             "FY20말 현금", "FY21_영업활동CF", "FY21_투자활동CF", "FY21_재무활동CF", "FY21_기타CF",
             "FY21말 현금",]

    df_cf_waterfall = pd.DataFrame(index=index_cf)

    for 대상 in graph_대상:
        df_대상 = df[(df['company'] == 대상)]
        column_cf = []

        FY18말현금_value = ""
        FY19영업활동CF_value = ""
        FY19투자활동CF_value = ""
        FY19재무활동CF_value = ""
        FY19기타CF_value = ""
        FY19말현금_value = ""

        FY20영업활동CF_value = ""
        FY20투자활동CF_value = ""
        FY20재무활동CF_value = ""
        FY20기타CF_value = ""
        FY20말현금_value = ""

        FY21영업활동CF_value = ""
        FY21투자활동CF_value = ""
        FY21재무활동CF_value = ""
        FY21기타CF_value = ""
        FY21말현금_value = ""

        ##19년도
        FY18말현금_value = df_대상[(df_대상['account'] == names_cf['기초CF'])]['FY19'].values[0]
        FY19영업활동CF_value = df_대상[(df_대상['account'] == names_cf['영업활동CF'])]['FY19'].values[0]
        FY19투자활동CF_value = df_대상[(df_대상['account'] == names_cf['투자활동CF'])]['FY19'].values[0]
        FY19재무활동CF_value = df_대상[(df_대상['account'] == names_cf['재무활동CF'])]['FY19'].values[0]

        #FY19말현금
        if df_대상[(df_대상['account'] == names_cf['기말CF'])]['FY19'].isnull().sum() == False :
            FY19말현금_value = df_대상[(df_대상['account'] == names_cf['기말CF'])]['FY19'].values[0]
        else:
            FY19말현금_value = df_대상[(df_대상['account'] == names_cf['기초CF'])]['FY20'].values[0]

        #FY19기타CF
        try:
            FY19기타CF_value = FY19말현금_value - FY18말현금_value - (FY19영업활동CF_value + FY19투자활동CF_value + FY19재무활동CF_value)
        except:
            pass

        ##20년도
        FY20영업활동CF_value = df_대상[(df_대상['account'] == names_cf['영업활동CF'])]['FY20'].values[0]
        FY20투자활동CF_value = df_대상[(df_대상['account'] == names_cf['투자활동CF'])]['FY20'].values[0]
        FY20재무활동CF_value = df_대상[(df_대상['account'] == names_cf['재무활동CF'])]['FY20'].values[0]

        #FY20말현금
        if df_대상[(df_대상['account'] == names_cf['기말CF'])]['FY20'].isnull().sum() == False:
            FY20말현금_value = df_대상[(df_대상['account'] == names_cf['기말CF'])]['FY20'].values[0]
        else:
            FY20말현금_value = df_대상[(df_대상['account'] == names_cf['기초CF'])]['FY21'].values[0]

        #FY20기타CF
        try:
            FY20기타CF_value = FY20말현금_value - FY19말현금_value - (FY20영업활동CF_value + FY20투자활동CF_value + FY20재무활동CF_value)
        except:
            pass

        ##21년도
        FY21영업활동CF_value = df_대상[(df_대상['account'] == names_cf['영업활동CF'])]['FY21'].values[0]
        FY21투자활동CF_value = df_대상[(df_대상['account'] == names_cf['투자활동CF'])]['FY21'].values[0]
        FY21재무활동CF_value = df_대상[(df_대상['account'] == names_cf['재무활동CF'])]['FY21'].values[0]
        FY21말현금_value = df_대상[(df_대상['account'] == names_cf['기말CF'])]['FY21'].values[0]

        #FY21기타CF
        try:
            FY21기타CF_value = FY21말현금_value - FY20말현금_value - (FY21영업활동CF_value + FY21투자활동CF_value + FY21재무활동CF_value)
        except:
            pass

        column_cf.append(FY18말현금_value)
        column_cf.append(FY19영업활동CF_value)
        column_cf.append(FY19투자활동CF_value)
        column_cf.append(FY19재무활동CF_value)
        column_cf.append(FY19기타CF_value)
        column_cf.append(FY19말현금_value)

        column_cf.append(FY20영업활동CF_value)
        column_cf.append(FY20투자활동CF_value)
        column_cf.append(FY20재무활동CF_value)
        column_cf.append(FY20기타CF_value)
        column_cf.append(FY20말현금_value)

        column_cf.append(FY21영업활동CF_value)
        column_cf.append(FY21투자활동CF_value)
        column_cf.append(FY21재무활동CF_value)
        column_cf.append(FY21기타CF_value)
        column_cf.append(FY21말현금_value)


        df_cf_waterfall[대상] = column_cf

    return df_cf_waterfall