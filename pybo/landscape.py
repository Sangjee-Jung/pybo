import json
import mpld3
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import pandas as pd
import numpy as np

def load_industry():

    #Raw Data Load
    df_산업코드_기업 = pd.read_excel('static/산점도분석_List_개발버전.xlsx', sheet_name='기업코드')
    df_산업코드_산업 = pd.read_excel('static/산점도분석_List_개발버전.xlsx', sheet_name='산업코드(전체)')

    company_name_all = df_산업코드_기업['회사명'].tolist()
    company_code_all_가공전 = df_산업코드_기업['종목코드'].tolist()
    company_code_all = []
    for code in company_code_all_가공전:
        company_code_all.append(code[1:7])


    return df_산업코드_산업, df_산업코드_기업, company_name_all, company_code_all

def define_industry(target, df_산업코드_산업, df_산업코드_기업):

    industry_code_lv2 = int(df_산업코드_기업.loc[df_산업코드_기업['회사명'] == target]['Lv2. 업종'].tolist()[0])
    industry_name_lv2 = df_산업코드_기업.loc[df_산업코드_기업['회사명'] == target]['Lv2. 업종명'].tolist()[0]

    industry_code_lv3 = int(df_산업코드_기업.loc[df_산업코드_기업['회사명'] == target]['Lv3. 업종'].tolist()[0])
    industry_name_lv3 = df_산업코드_기업.loc[df_산업코드_기업['회사명'] == target]['Lv3. 업종명'].tolist()[0]

    industry_code_lv4 = int(df_산업코드_기업.loc[df_산업코드_기업['회사명'] == target]['Lv4. 업종'].tolist()[0])
    industry_name_lv4 = df_산업코드_기업.loc[df_산업코드_기업['회사명'] == target]['Lv4. 업종명'].tolist()[0]


    #Industry 생성
    for i in range(len(df_산업코드_산업['CODE'])):
        if df_산업코드_산업["CODE"][i] == industry_code_lv2 and df_산업코드_산업["Lv"][i] == 2:
            for j in range(i+1, 2000):
                if df_산업코드_산업["Lv"][j] == 2 or df_산업코드_산업["Lv"][j] == 1:
                    df_industry_code_lv2 = df_산업코드_산업.iloc[i:j, 0:4]
                    break
            break

    return industry_code_lv2, industry_name_lv2, df_industry_code_lv2, industry_code_lv4, industry_name_lv4, industry_code_lv3, industry_name_lv3

def define_companies(search_code, level, fs_type):

    df_산업코드_기업 = pd.read_excel('static/산점도분석_List_개발버전.xlsx', sheet_name='기업코드')
    df_산업코드_산업 = pd.read_excel('static/산점도분석_List_개발버전.xlsx', sheet_name='산업코드(전체)')

    for i in range(len(df_산업코드_산업["CODE"])):
        if str(int(df_산업코드_산업['CODE'][i])) == search_code:
            search_name = df_산업코드_산업['표준산업분류(한글)'][i]
            break

    companies = []
    for i in range(len(df_산업코드_기업)):
        try:
            if str(int(df_산업코드_기업["한국표준산업분류코드"][i]))[0: level+1 ] == search_code:
                companies.append(df_산업코드_기업['회사명'][i])
        except:
            pass

    #데이터프레임 생성

    if fs_type == "별도":
        dart_is_4 = pd.read_excel("static/dart_is_4.xlsx", sheet_name='별도', header=0)
    else:
        dart_is_4 = pd.read_excel("static/dart_is_4.xlsx", sheet_name='연결', header=0)

    df = dart_is_4

    영업이익_2022_LTM = []
    영업이익_2021 = []
    영업이익_2020 = []
    영업이익_2019 = []
    매출액_2022_LTM = []
    매출액_2021 = []
    매출액_2020 = []
    매출액_2019 = []

    for company in companies:
        ebit_row = df[(df['company'] == company) & (df['account'] == "dart_OperatingIncomeLoss")]
        try:
            영업이익_2022_LTM.append(int(ebit_row['FY22_9M_LTM']))
        except:
            영업이익_2022_LTM.append(np.nan)
        try:
            영업이익_2021.append(int(ebit_row['FY21']))
        except:
            영업이익_2021.append(np.nan)
        try:
            영업이익_2020.append(int(ebit_row['FY20']))
        except:
            영업이익_2020.append(np.nan)
        try:
            영업이익_2019.append(int(ebit_row['FY19']))
        except:
            영업이익_2019.append(np.nan)

        revenue_row = df[(df['company'] == company) & (df['account'] == "ifrs-full_Revenue")]
        if len(revenue_row) == 0:
            revenue_row = df[(df['company'] == company) & (df['account'] == "ifrs-full_GrossProfit")]

        try:
            매출액_2022_LTM.append(int((revenue_row['FY22_9M_LTM'])))
        except:
            매출액_2022_LTM.append(np.nan)
        try:
            매출액_2021.append(int((revenue_row['FY21'])))
        except:
            매출액_2021.append(np.nan)
        try:
            매출액_2020.append(int(revenue_row['FY20']))
        except:
            매출액_2020.append(np.nan)
        try:
            매출액_2019.append(int(revenue_row['FY19']))
        except:
            매출액_2019.append(np.nan)

    dict_data = {'매출액_2019': 매출액_2019, '매출액_2020': 매출액_2020, '매출액_2021': 매출액_2021, '매출액_2022_LTM': 매출액_2022_LTM,
                 '영업이익_2019': 영업이익_2019, '영업이익_2020': 영업이익_2020, '영업이익_2021': 영업이익_2021, '영업이익_2022_LTM': 영업이익_2022_LTM}

    df = pd.DataFrame(dict_data, index=companies)
    df = df.astype('float')

    영업이익률_2021 = []
    for i in range(len(companies)):
        try:
            영업이익률_2021.append(df['영업이익_2021'][i] / df['매출액_2021'][i] * 100)
        except:
            영업이익률_2021.append(np.nan)

    df["영업이익률_2021"] = 영업이익률_2021
    df["순위"] = df['매출액_2021'].rank(ascending = False, numeric_only = True)
    df = df.sort_values(by=['순위'], axis=0)

    return search_name, companies, df

def make_df_customized(x축,y축,graph_대상, fs_type, size):

    if fs_type == "별도":
        df = pd.read_excel("static/dart_fs.xlsx", sheet_name='별도', header=0)
    else:
        df = pd.read_excel("static/dart_fs.xlsx", sheet_name='연결', header=0)


    x축_2022_LTM = []
    x축_2021 = []
    x축_2020 = []
    x축_2019 = []
    y축_2022_LTM = []
    y축_2021 = []
    y축_2020 = []
    y축_2019 = []
    size_2022_LTM = []
    size_2021 = []
    size_2020 = []
    size_2019 = []

    이익률 = ['GP%', 'EBIT%', 'NI%']
    성장률 = ['Revenue_growth%', 'EBIT_growth%', 'NI_growth%']

    names_further = {'GP%': 'ifrs-full_GrossProfit', 'EBIT%': 'dart_OperatingIncomeLoss', 'NI%': 'ifrs-full_ProfitLoss',
                     'Revenue_growth%': 'ifrs-full_Revenue', 'EBIT_growth%': 'dart_OperatingIncomeLoss', 'NI_growth%': 'ifrs-full_ProfitLoss', }

    for 대상 in graph_대상:

        #x축
        if x축 in 이익률:
            x축_분모_row = df[(df['company'] == 대상) & (df['account'] == 'ifrs-full_Revenue')]
            x축_분자_row = df[(df['company'] == 대상) & (df['account'] == names_further[x축])]

            try:
                x축_2022_LTM.append(int(x축_분자_row['FY22_9M_LTM'])/int(x축_분모_row['FY22_9M_LTM']) * 100)
            except:
                x축_2022_LTM.append(np.nan)
            try:
                x축_2021.append(int(x축_분자_row['FY21'])/int(x축_분모_row['FY21']) * 100)
            except:
                x축_2021.append(np.nan)
            try:
                x축_2020.append(int(x축_분자_row['FY20'])/int(x축_분모_row['FY20']) * 100)
            except:
                x축_2020.append(np.nan)
            try:
                x축_2019.append(int(x축_분자_row['FY19'])/int(x축_분모_row['FY19']) * 100)
            except:
                x축_2019.append(np.nan)

        elif x축 in 성장률:
            x축_row = df[(df['company'] == 대상) & (df['account'] == names_further[x축])]

            try:
                x축_2022_LTM.append(((int(x축_row['FY22_9M_LTM'])/int(x축_row['FY21']))-1) * 100)
            except:
                x축_2022_LTM.append(np.nan)
            try:
                x축_2021.append(((int(x축_row['FY21'])/int(x축_row['FY20']))-1) * 100)
            except:
                x축_2021.append(np.nan)
            try:
                x축_2020.append(((int(x축_row['FY20'])/int(x축_row['FY19']))-1) * 100)
            except:
                x축_2020.append(np.nan)
            try:
                x축_2019.append(((int(x축_row['FY19'])/int(x축_row['FY18']))-1) * 100)
            except:
                x축_2019.append(np.nan)

        else:
            x축_row = df[(df['company'] == 대상) & (df['account'] == x축)]
            try:
                x축_2022_LTM.append(int(x축_row['FY22_9M_LTM']))
            except:
                x축_2022_LTM.append(np.nan)
            try:
                x축_2021.append(int(x축_row['FY21']))
            except:
                x축_2021.append(np.nan)
            try:
                x축_2020.append(int(x축_row['FY20']))
            except:
                x축_2020.append(np.nan)
            try:
                x축_2019.append(int(x축_row['FY19']))
            except:
                x축_2019.append(np.nan)

        #y축
        if y축 in 이익률:
            y축_분모_row = df[(df['company'] == 대상) & (df['account'] == 'ifrs-full_Revenue')]
            y축_분자_row = df[(df['company'] == 대상) & (df['account'] == names_further[y축])]

            try:
                y축_2022_LTM.append(int(y축_분자_row['FY22_9M_LTM']) / int(y축_분모_row['FY22_9M_LTM']) * 100)
            except:
                y축_2022_LTM.append(np.nan)
            try:
                y축_2021.append(int(y축_분자_row['FY21']) / int(y축_분모_row['FY21']) * 100)
            except:
                y축_2021.append(np.nan)
            try:
                y축_2020.append(int(y축_분자_row['FY20']) / int(y축_분모_row['FY20']) * 100)
            except:
                y축_2020.append(np.nan)
            try:
                y축_2019.append(int(y축_분자_row['FY19']) / int(y축_분모_row['FY19']) * 100)
            except:
                y축_2019.append(np.nan)


        elif y축 in 성장률:
            y축_row = df[(df['company'] == 대상) & (df['account'] == names_further[y축])]

            try:
                y축_2022_LTM.append(((int(y축_row['FY22_9M_LTM']) / int(y축_row['FY21'])) - 1) * 100)
            except:
                y축_2022_LTM.append(np.nan)
            try:
                y축_2021.append(((int(y축_row['FY21']) / int(y축_row['FY20'])) - 1) * 100)
            except:
                y축_2021.append(np.nan)
            try:
                y축_2020.append(((int(y축_row['FY20']) / int(y축_row['FY19'])) - 1) * 100)
            except:
                y축_2020.append(np.nan)
            try:
                y축_2019.append(((int(y축_row['FY19']) / int(y축_row['FY18'])) - 1) * 100)
            except:
                y축_2019.append(np.nan)


        else:
            y축_row = df[(df['company'] == 대상) & (df['account'] == y축)]
            try:
                y축_2022_LTM.append(int(y축_row['FY22_9M_LTM']))
            except:
                y축_2022_LTM.append(np.nan)
            try:
                y축_2021.append(int(y축_row['FY21']))
            except:
                y축_2021.append(np.nan)
            try:
                y축_2020.append(int(y축_row['FY20']))
            except:
                y축_2020.append(np.nan)
            try:
                y축_2019.append(int(y축_row['FY19']))
            except:
                y축_2019.append(np.nan)

        #size
        if size == "n/a":
            pass
        else:
            size_row = df[(df['company'] == 대상) & (df['account'] == size)]
            try:
                size_2022_LTM.append(int(size_row['FY22_9M_LTM']))
            except:
                size_2022_LTM.append(np.nan)
            try:
                size_2021.append(int(size_row['FY21']))
            except:
                size_2021.append(np.nan)
            try:
                size_2020.append(int(size_row['FY20']))
            except:
                size_2020.append(np.nan)
            try:
                size_2019.append(int(size_row['FY19']))
            except:
                size_2019.append(np.nan)


    if size == "n/a":
        dict_data = {'x축_2019': x축_2019, 'x축_2020': x축_2020, 'x축_2021': x축_2021, 'x축_2022_LTM': x축_2022_LTM,
                     'y축_2019': y축_2019, 'y축_2020': y축_2020, 'y축_2021': y축_2021, 'y축_2022_LTM': y축_2022_LTM,}
    else:
        dict_data = {'x축_2019': x축_2019, 'x축_2020': x축_2020, 'x축_2021': x축_2021, 'x축_2022_LTM': x축_2022_LTM,
                     'y축_2019': y축_2019, 'y축_2020': y축_2020, 'y축_2021': y축_2021, 'y축_2022_LTM': y축_2022_LTM,
                     'size_2019': size_2019, 'size_2020': size_2020, 'size_2021': size_2021, 'size_2022_LTM': size_2022_LTM}

    df_customized = pd.DataFrame(dict_data, index=graph_대상)
    df_customized = df_customized.astype('float')

    return df_customized

def make_scatter(df):

    #색상설정
    kpmg_blue = '#00338D'
    medium_blue = '#005EB8'
    light_blue = '#0091DA'
    violet = '#483698'
    purple = '#470A68'
    light_purple = '#6D2077'
    green = '#00A3A1'

    color_kpmg = [light_blue, medium_blue, light_purple, green]

    #######################그래프그리기##########################
    # 그래프 설정
    f = plt.figure(figsize=(17, 10))
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False
    plt.rc('font', size=13)

    # 결측치 제거된 DataFrame 생성
    df_2021 = df[['매출액_2021', '영업이익_2021', '영업이익률_2021', '순위','index']]
    df_2021.dropna(how="any")


    df_2020 = df[['매출액_2020', '영업이익_2020']]
    df_2020.dropna(how="any")

    df_2019 = df[['매출액_2019', '영업이익_2019']]
    df_2019.dropna(how="any")

    df_2022_LTM = df[['매출액_2022_LTM', '영업이익_2022_LTM']]
    df_2022_LTM.dropna(how="any")

    # 산점도 그래프 그리기
    plt.scatter(df_2022_LTM['매출액_2022_LTM'], df_2022_LTM['영업이익_2022_LTM'], color=color_kpmg[3])
    plt.scatter(df_2021['매출액_2021'], df_2021['영업이익_2021'], color=color_kpmg[0])
    plt.scatter(df_2020['매출액_2020'], df_2020['영업이익_2020'], color=color_kpmg[1])
    plt.scatter(df_2019['매출액_2019'], df_2019['영업이익_2019'], color=color_kpmg[2])


    # 연결선 그리기
    df_arrow1 = df[['매출액_2021', '영업이익_2021', '매출액_2020', '영업이익_2020']]
    df_arrow1.dropna(how="any")

    for i in range(len(df_arrow1)):
        plt.plot([df_arrow1['매출액_2021'][i], df_arrow1['매출액_2020'][i]], [df_arrow1['영업이익_2021'][i],df_arrow1['영업이익_2020'][i]], color='black', alpha=0.2)

    df_arrow2 = df[['매출액_2020', '영업이익_2020', '매출액_2019', '영업이익_2019']]
    df_arrow2.dropna(how="any")

    for i in range(len(df_arrow2)):
        plt.plot([df_arrow2['매출액_2020'][i], df_arrow2['매출액_2019'][i]], [df_arrow2['영업이익_2020'][i], df_arrow2['영업이익_2019'][i]], color='black', alpha=0.2)

    df_arrow3 = df[['매출액_2022_LTM', '영업이익_2022_LTM', '매출액_2021', '영업이익_2021']]
    df_arrow3.dropna(how="any")

    for i in range(len(df_arrow3)):
        plt.plot([df_arrow3['매출액_2022_LTM'][i], df_arrow3['매출액_2021'][i]],
                 [df_arrow3['영업이익_2022_LTM'][i], df_arrow3['영업이익_2021'][i]], color='black', linestyle='--', alpha=0.2)


    # x축 설정
    xmax = plt.axis()[1]
    plt.xlim(0, xmax)

    #회사명 표시
    for i in range(len(df_2021)):
        plt.text(df_2021['매출액_2021'][i] + xmax*0.005, df_2021['영업이익_2021'][i],
                 df_2021['index'][i] + "(" + str("%0.2f%%" % df_2021['영업이익률_2021'][i]) + ")")

    # 축, 범례 표시
    plt.xlabel('매출액', fontsize=17, labelpad=30)
    plt.ylabel('영업이익', fontsize=17, labelpad=45)
    plt.legend(['2022 LTM(9월기준)','2021', '2020', '2019'], fontsize=15, loc='upper left')

    # 수평선(영업이익=0) 표시
    plt.plot([0,xmax],[0,0], color='indianred', linestyle='--', linewidth=1.2, alpha=0.5)

    #HTML로 내보내기
    graph = mpld3.fig_to_html(f, figid='THIS_IS_FIGID')

    return graph


def make_scatter_customized(df, x축, y축, size, years):

    # 색상설정
    kpmg_blue = '#00338D'
    medium_blue = '#005EB8'
    light_blue = '#0091DA'
    violet = '#483698'
    purple = '#470A68'
    light_purple = '#6D2077'
    green = '#00A3A1'

    color_kpmg = [light_blue, medium_blue, light_purple, green]


    #######################그래프그리기##########################
    # 그래프 설정
    f = plt.figure(figsize=(17, 10))
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False
    plt.rc('font', size=13)


    # 결측치 제거된 DataFrame 생성
    df_2021 = df[['x축_2021', 'y축_2021']]
    df_2021.dropna(how="any")

    df_2020 = df[['x축_2020', 'y축_2020']]
    df_2020.dropna(how="any")

    df_2019 = df[['x축_2019', 'y축_2019']]
    df_2019.dropna(how="any")

    df_2022_LTM = df[['x축_2022_LTM', 'y축_2022_LTM']]
    df_2022_LTM.dropna(how="any")

    index = df.index.to_list()

    # size 지정
    if size == "n/a":
        pass
    else:
        resized_2022_LTM = []
        resized_2021 = []
        resized_2020 = []
        resized_2019 = []

        #Scale 설정
        size_all = []
        for i in range(len(index)):
            if 2022 in years:
                size_all.append(int(df['size_2022_LTM'][i]))
            else:
                pass

            if 2021 in years:
                size_all.append(int(df['size_2021'][i]))
            else:
                pass

            if 2020 in years:
                size_all.append(int(df['size_2020'][i]))
            else:
                pass

            if 2019 in years:
                size_all.append(int(df['size_2019'][i]))
            else:
                pass

        size_max = max(size_all)

        # size 재지정
        for i in range(len(index)):
            try:
                if df['size_2022_LTM'][i] > 0:
                    resized_2022_LTM.append((int(df['size_2022_LTM'][i])/size_max * 9964)+36)
                else:
                    resized_2022_LTM.append(36)
            except:
                resized_2022_LTM.append(np.nan)
            try:
                if df['size_2021'][i] > 0:
                    resized_2021.append((int(df['size_2021'][i])/size_max * 9964)+36)
                else:
                    resized_2021.append(36)
            except:
                resized_2021.append(np.nan)
            try:
                if df['size_2020'][i] > 0:
                    resized_2020.append((int(df['size_2020'][i])/size_max * 9964)+36)
                else:
                    resized_2020.append(36)
            except:
                resized_2020.append(np.nan)
            try:
                if df['size_2019'][i] >0:
                    resized_2019.append((int(df['size_2019'][i])/size_max * 9964) + 36)
                else:
                    resized_2019.append(36)
            except:
                resized_2019.append(np.nan)


    # 산점도 그래프 그리기
    if size == "n/a":
        if 2022 in years:
            plt.scatter(df_2022_LTM['x축_2022_LTM'], df_2022_LTM['y축_2022_LTM'], color=color_kpmg[3])
        else:
            pass
        if 2021 in years:
            plt.scatter(df_2021['x축_2021'], df_2021['y축_2021'], color=color_kpmg[0])
        else:
            pass
        if 2020 in years:
            plt.scatter(df_2020['x축_2020'], df_2020['y축_2020'], color=color_kpmg[1])
        else:
            pass
        if 2019 in years:
            plt.scatter(df_2019['x축_2019'], df_2019['y축_2019'], color=color_kpmg[2])
        else:
            pass
    else:
        if 2022 in years:
            try:
                plt.scatter(df_2022_LTM['x축_2022_LTM'], df_2022_LTM['y축_2022_LTM'], color=color_kpmg[3], s=resized_2022_LTM, alpha=0.9)
            except:
                plt.scatter(df_2022_LTM['x축_2022_LTM'], df_2022_LTM['y축_2022_LTM'], color=color_kpmg[3], alpha=0.9)
        else:
            pass

        if 2021 in years:
            try:
                plt.scatter(df_2021['x축_2021'], df_2021['y축_2021'], color=color_kpmg[0], s=resized_2021, alpha=0.7)
            except:
                plt.scatter(df_2021['x축_2021'], df_2021['y축_2021'], color=color_kpmg[0], alpha=0.7)
        else:
            pass

        if 2020 in years:
            try:
                plt.scatter(df_2020['x축_2020'], df_2020['y축_2020'], color=color_kpmg[1], s=resized_2020, alpha=0.6)
            except:
                plt.scatter(df_2020['x축_2020'], df_2020['y축_2020'], color=color_kpmg[1], alpha=0.6)
        else:
            pass

        if 2019 in years:
            try:
                plt.scatter(df_2019['x축_2019'], df_2019['y축_2019'], color=color_kpmg[2], s=resized_2019, alpha=0.5)
            except:
                plt.scatter(df_2019['x축_2019'], df_2019['y축_2019'], color=color_kpmg[2], alpha=0.5)
        else:
            pass


    # 연결선 그리기
    if (2021 in years) and (2020 in years):
        df_arrow1 = df[['x축_2021', 'y축_2021', 'x축_2020', 'y축_2020']]
        df_arrow1.dropna(how="any")

        for i in range(len(df_arrow1)):
            plt.plot([df_arrow1['x축_2021'][i], df_arrow1['x축_2020'][i]],
                     [df_arrow1['y축_2021'][i], df_arrow1['y축_2020'][i]], color='black', alpha=0.2)
    else:
        pass

    if (2020 in years) and (2019 in years):
        df_arrow2 = df[['x축_2020', 'y축_2020', 'x축_2019', 'y축_2019']]
        df_arrow2.dropna(how="any")

        for i in range(len(df_arrow2)):
            plt.plot([df_arrow2['x축_2020'][i], df_arrow2['x축_2019'][i]],
                     [df_arrow2['y축_2020'][i], df_arrow2['y축_2019'][i]], color='black', alpha=0.2)
    else:
        pass

    if (2022 in years) and (2021 in years):
        df_arrow3 = df[['x축_2022_LTM', 'y축_2022_LTM', 'x축_2021', 'y축_2021']]
        df_arrow3.dropna(how="any")

        for i in range(len(df_arrow3)):
            plt.plot([df_arrow3['x축_2022_LTM'][i], df_arrow3['x축_2021'][i]],
                     [df_arrow3['y축_2022_LTM'][i], df_arrow3['y축_2021'][i]], color='black', linestyle='--', alpha=0.2)
    else:
        pass


    # x축 설정
    xmax = plt.axis()[1]
    plt.xlim(0, xmax)

    # 회사명 표시
    for i in range(len(df_2021)):
        plt.text(df_2021['x축_2021'][i] + xmax*0.005, df_2021['y축_2021'][i],
                 index[i])

    # Dictionary 설정

    names = {'ifrs-full_Revenue': '매출액', 'ifrs-full_CostOfSales': '매출원가', 'ifrs-full_GrossProfit': '매출총이익',
             'dart_TotalSellingGeneralAdministrativeExpenses': '판매비와관리비', 'dart_OperatingIncomeLoss': '영업이익',
             'ifrs-full_ProfitLoss': '당기순이익', 'ifrs-full_Assets': '총자산', 'ifrs-full_Liabilities': '총부채', 'ifrs-full_Equity': '총자본',
             'ifrs-full_CashFlowsFromUsedInOperatingActivities': '영업활동CF', 'ifrs-full_CashFlowsFromUsedInInvestingActivities': '투자활동CF',
             'ifrs-full_CashFlowsFromUsedInFinancingActivities': '재무활동CF',
             'GP%': '매출총이익률', 'EBIT%': '영업이익률', 'NI%': '당기순이익률',
             'Revenue_growth%': '매출증가율', 'EBIT_growth%': '영업이익증가율', 'NI_growth%': '당기순이익증가율',}

    name_x축 = names[x축]
    name_y축 = names[y축]

    # 축, 범례 표시
    plt.xlabel(name_x축, fontsize=17, labelpad=30)
    plt.ylabel(name_y축, fontsize=17, labelpad=45)

    #legend 표시
    if size == "n/a":
        plt.legend(['2022 LTM(9월기준)','2021', '2020', '2019'], fontsize=15, loc='upper left')
    else:
        pass

    # 수평선(영업이익=0) 표시
    plt.plot([0, xmax], [0, 0], color='indianred', linestyle='--', linewidth=1.2, alpha=0.5)

    # HTML로 내보내기
    graph_customized = mpld3.fig_to_html(f, figid='THIS_IS_FIGID')

    return graph_customized, name_x축, name_y축