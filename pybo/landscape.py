import json
import mpld3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def load_industry():

    #Raw Data Load
    df_산업코드_기업 = pd.read_excel('static/산점도분석_List_개발버전.xlsx', sheet_name='기업코드')
    df_산업코드_산업 = pd.read_excel('static/산점도분석_List_개발버전.xlsx', sheet_name='산업코드(전체)')

    return df_산업코드_산업, df_산업코드_기업

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

def define_companies(search_code, level):

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
    dart_is_3 = pd.read_excel("static/dart_is_3.xlsx", header=0)

    df = dart_is_3

    영업이익_2021 = []
    영업이익_2020 = []
    영업이익_2019 = []
    매출액_2021 = []
    매출액_2020 = []
    매출액_2019 = []

    for company in companies:
        ebit_row = df[(df['company'] == company) & (df['account'] == "dart_OperatingIncomeLoss")]
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

    dict_data = {'매출액_2021': 매출액_2021, '영업이익_2021': 영업이익_2021,
                 '매출액_2020': 매출액_2020, '영업이익_2020': 영업이익_2020,
                 '매출액_2019': 매출액_2019, '영업이익_2019': 영업이익_2019}

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

def make_scatter(df, search_name):

    #색상설정
    kpmg_blue = '#00338D'
    medium_blue = '#005EB8'
    light_blue = '#0091DA'
    violet = '#483698'
    purple = '#470A68'
    light_purple = '#6D2077'
    green = '#00A3A1'

    color_kpmg = [light_blue, medium_blue, light_purple]

    #######################그래프그리기##########################
    # 그래프 설정
    f = plt.figure(figsize=(18, 10))
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


    # 산점도 그래프 그리기
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
    plt.legend(['2021', '2020', '2019'], fontsize=15, loc='upper left')

    # 수평선(영업이익=0) 표시
    plt.plot([0,xmax],[0,0], color='indianred', linestyle='--', linewidth=1.2, alpha=0.5)

    #HTML로 내보내기
    graph = mpld3.fig_to_html(f, figid='THIS_IS_FIGID')

    return graph