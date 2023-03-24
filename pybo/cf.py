import json
import mpld3
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker

def make_df_cf_waterfall(graph_대상, fs_type):

    if fs_type == "별도":
        df = pd.read_excel("static/dart_fs.xlsx", sheet_name='별도', header=0)
    else:
        df = pd.read_excel("static/dart_fs.xlsx", sheet_name='연결', header=0)


    names_cf = {'영업CF': 'ifrs-full_CashFlowsFromUsedInOperatingActivities',
                '투자CF': 'ifrs-full_CashFlowsFromUsedInInvestingActivities',
                '재무CF': 'ifrs-full_CashFlowsFromUsedInFinancingActivities',
                '기초CF': 'dart_CashAndCashEquivalentsAtBeginningOfPeriodCf',
                '기말CF': 'dart_CashAndCashEquivalentsAtEndOfPeriodCf',}


    index_cf= ["FY18말 현금","영업CF(19)","투자CF(19)","재무CF(19)","기타CF(19)",
             "FY19말 현금", "영업CF(20)", "투자CF(20)", "재무CF(20)", "기타CF(20)",
             "FY20말 현금", "영업CF(21)", "투자CF(21)", "재무CF(21)", "기타CF(21)",
             "FY21말 현금",]

    df_cf_waterfall = pd.DataFrame(index=index_cf)

    for 대상 in graph_대상:
        df_대상 = df[(df['company'] == 대상)]
        column_cf = []

        FY18말현금_value = ""
        FY19영업CF_value = ""
        FY19투자CF_value = ""
        FY19재무CF_value = ""
        FY19기타CF_value = ""
        FY19말현금_value = ""

        FY20영업CF_value = ""
        FY20투자CF_value = ""
        FY20재무CF_value = ""
        FY20기타CF_value = ""
        FY20말현금_value = ""

        FY21영업CF_value = ""
        FY21투자CF_value = ""
        FY21재무CF_value = ""
        FY21기타CF_value = ""
        FY21말현금_value = ""

        ##19년도
        FY18말현금_value = df_대상[(df_대상['account'] == names_cf['기초CF'])]['FY19'].values[0]
        FY19영업CF_value = df_대상[(df_대상['account'] == names_cf['영업CF'])]['FY19'].values[0]
        FY19투자CF_value = df_대상[(df_대상['account'] == names_cf['투자CF'])]['FY19'].values[0]
        FY19재무CF_value = df_대상[(df_대상['account'] == names_cf['재무CF'])]['FY19'].values[0]

        #FY19말현금
        if df_대상[(df_대상['account'] == names_cf['기말CF'])]['FY19'].isnull().sum() == False :
            FY19말현금_value = df_대상[(df_대상['account'] == names_cf['기말CF'])]['FY19'].values[0]
        else:
            FY19말현금_value = df_대상[(df_대상['account'] == names_cf['기초CF'])]['FY20'].values[0]

        #FY19기타CF
        try:
            FY19기타CF_value = FY19말현금_value - FY18말현금_value - (FY19영업CF_value + FY19투자CF_value + FY19재무CF_value)
        except:
            pass

        ##20년도
        FY20영업CF_value = df_대상[(df_대상['account'] == names_cf['영업CF'])]['FY20'].values[0]
        FY20투자CF_value = df_대상[(df_대상['account'] == names_cf['투자CF'])]['FY20'].values[0]
        FY20재무CF_value = df_대상[(df_대상['account'] == names_cf['재무CF'])]['FY20'].values[0]

        #FY20말현금
        if df_대상[(df_대상['account'] == names_cf['기말CF'])]['FY20'].isnull().sum() == False:
            FY20말현금_value = df_대상[(df_대상['account'] == names_cf['기말CF'])]['FY20'].values[0]
        else:
            FY20말현금_value = df_대상[(df_대상['account'] == names_cf['기초CF'])]['FY21'].values[0]

        #FY20기타CF
        try:
            FY20기타CF_value = FY20말현금_value - FY19말현금_value - (FY20영업CF_value + FY20투자CF_value + FY20재무CF_value)
        except:
            pass

        ##21년도
        FY21영업CF_value = df_대상[(df_대상['account'] == names_cf['영업CF'])]['FY21'].values[0]
        FY21투자CF_value = df_대상[(df_대상['account'] == names_cf['투자CF'])]['FY21'].values[0]
        FY21재무CF_value = df_대상[(df_대상['account'] == names_cf['재무CF'])]['FY21'].values[0]
        FY21말현금_value = df_대상[(df_대상['account'] == names_cf['기말CF'])]['FY21'].values[0]

        #FY21기타CF
        try:
            FY21기타CF_value = FY21말현금_value - FY20말현금_value - (FY21영업CF_value + FY21투자CF_value + FY21재무CF_value)
        except:
            pass

        column_cf.append(FY18말현금_value)
        column_cf.append(FY19영업CF_value)
        column_cf.append(FY19투자CF_value)
        column_cf.append(FY19재무CF_value)
        column_cf.append(FY19기타CF_value)
        column_cf.append(FY19말현금_value)

        column_cf.append(FY20영업CF_value)
        column_cf.append(FY20투자CF_value)
        column_cf.append(FY20재무CF_value)
        column_cf.append(FY20기타CF_value)
        column_cf.append(FY20말현금_value)

        column_cf.append(FY21영업CF_value)
        column_cf.append(FY21투자CF_value)
        column_cf.append(FY21재무CF_value)
        column_cf.append(FY21기타CF_value)
        column_cf.append(FY21말현금_value)


        df_cf_waterfall[대상] = column_cf

    return df_cf_waterfall

def make_graph_cf_waterfall(df_cf_waterfall, graph_대상):

    # 색상설정
    kpmg_blue = '#00338D'
    medium_blue = '#005EB8'
    light_blue = '#0091DA'
    violet = '#483698'
    purple = '#470A68'
    light_purple = '#6D2077'
    green = '#00A3A1'

    colors_using = [kpmg_blue, light_blue, light_purple]

    #그래프 설정
    f = plt.figure(figsize=(17, 6 * len(graph_대상)))
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False
    plt.rc('font', size=13)

    label = df_cf_waterfall.index.tolist()
    index = np.arange(len(label))


    for i, 대상 in enumerate(graph_대상):

        # 누적 구하기
        CF = df_cf_waterfall[대상].tolist()
        누적 = []

        sum = 0
        for j in range(0,5):
            sum += CF[j]
            누적.append(sum)

        sum = 0
        for j in range(5, 10):
            sum += CF[j]
            누적.append(sum)

        sum = 0
        for j in range(10, 15):
            sum += CF[j]
            누적.append(sum)

        누적.append(0)

        # 그외 구하기
        bottom_양 = []
        bottom_음 = []
        cashflow_양 = []
        cashflow_음 = []
        colors = []

        for k in range(0, 16):
            #현금잔액
            if k in [0,5,10,15]:
                bottom_양.append(0)
                bottom_음.append(0)
                cashflow_양.append(CF[k])
                cashflow_음.append(0)
                colors.append(colors_using[0])
            else:
                #조건1:
                if 누적[k-1] >= 0 and 누적[k] >= 0 and CF[k] >= 0:
                    bottom_양.append(누적[k-1])
                    bottom_음.append(0)
                    cashflow_양.append(CF[k])
                    cashflow_음.append(0)
                    colors.append(colors_using[1])
                #조건2:
                elif 누적[k-1] >= 0 and 누적[k] >= 0 and CF[k] < 0:
                    bottom_양.append(누적[k])
                    bottom_음.append(0)
                    cashflow_양.append(-CF[k])
                    cashflow_음.append(0)
                    colors.append(colors_using[2])
                # 조건3:
                elif 누적[k-1] >= 0 and 누적[k] < 0 and CF[k] < 0:
                    bottom_양.append(0)
                    bottom_음.append(0)
                    cashflow_양.append(누적[k-1])
                    cashflow_음.append(CF[k] + 누적[k-1])
                    colors.append(colors_using[2])
                # 조건4:
                elif 누적[k-1] < 0 and 누적[k] >= 0 and CF[k] >= 0:
                    bottom_양.append(0)
                    bottom_음.append(0)
                    cashflow_양.append(CF[k] + 누적[k-1])
                    cashflow_음.append(누적[k-1])
                    colors.append(colors_using[1])
                # 조건5:
                elif 누적[k-1] < 0 and 누적[k] < 0 and CF[k] >= 0:
                    bottom_양.append(0)
                    bottom_음.append(누적[k])
                    cashflow_양.append(0)
                    cashflow_음.append(-CF[k])
                    colors.append(colors_using[1])
                # 조건6:
                elif 누적[k-1] < 0 and 누적[k] < 0 and CF[k] < 0:
                    bottom_양.append(0)
                    bottom_음.append(누적[k-1])
                    cashflow_양.append(0)
                    cashflow_음.append(CF[k])
                    colors.append(colors_using[2])

        #그래프 그리기
        ax = plt.subplot(len(graph_대상), 1, i + 1)

        ax.bar(index, bottom_양, width= 0.7, color = "white")
        ax.bar(index, cashflow_양, width=0.7, bottom= bottom_양, color= colors)
        ax.bar(index, bottom_음, width=0.7, color="white")
        ax.bar(index, cashflow_음, width=0.7, bottom=bottom_음, color = colors)


        ax.set_title(대상 + " Cash Flow", fontsize=17)
        ax.set_xticklabels(label)
        plt.xticks(index)

        # x축 설정
        xmax = plt.axis()[1]
        plt.xlim(-1, xmax)

        # 수평선(영업이익=0) 표시
        plt.plot([-1, xmax], [0, 0], color='indianred', linestyle='--', linewidth=1.2, alpha=0.4)

    graph = mpld3.fig_to_html(f, figid='THIS_IS_FIGID')

    return graph, bottom_양