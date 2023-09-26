import json
import mpld3
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import pandas as pd
import numpy as np
from matplotlib.patches import FancyArrowPatch

def make_scatter_external(df):

    #색상설정
    kpmg_blue = '#00338D'
    medium_blue = '#005EB8'
    light_blue = '#0091DA'
    violet = '#483698'
    purple = '#470A68'
    light_purple = '#6D2077'
    green = '#00A3A1'
    pink = '#E30276'

    color_kpmg = [light_blue, medium_blue, light_purple, green, pink]

    #######################그래프그리기##########################
    # 그래프 설정
    #f = plt.figure(figsize=(17, 10))
    fig, ax = plt.subplots(figsize=(17, 10))
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False
    plt.rc('font', size=13)

    # 결측치 제거된 DataFrame 생성

    df_2023 = df[['별도매출_23', '별도영업이익_23']]
    df_2023.dropna(how="any")

    df_2022 = df[['별도매출_22', '별도영업이익_22', 'Name']]
    df_2022.dropna(how="any")

    df_2021 = df[['별도매출_21', '별도영업이익_21']]
    df_2021.dropna(how="any")

    df_2020 = df[['별도매출_20', '별도영업이익_20']]
    df_2020.dropna(how="any")

    # 산점도 그래프 그리기
    plt.scatter(df_2023['별도매출_23'], df_2023['별도영업이익_23'], color=color_kpmg[4])
    plt.scatter(df_2022['별도매출_22'], df_2022['별도영업이익_22'], color=color_kpmg[3])
    plt.scatter(df_2021['별도매출_21'], df_2021['별도영업이익_21'], color=color_kpmg[0])
    plt.scatter(df_2020['별도매출_20'], df_2020['별도영업이익_20'], color=color_kpmg[1])

    # 연결선 그리기
    df_arrow1 = df[['별도매출_20', '별도영업이익_20', '별도매출_21', '별도영업이익_21']]
    df_arrow1.dropna(how="any")

    for i in range(len(df_arrow1)):
        plt.plot([df_arrow1['별도매출_21'].iloc[i], df_arrow1['별도매출_20'].iloc[i]], [df_arrow1['별도영업이익_21'].iloc[i], df_arrow1['별도영업이익_20'].iloc[i]], color='black', alpha=0.2)


    df_arrow2 = df[['별도매출_21', '별도영업이익_21', '별도매출_22', '별도영업이익_22']]
    df_arrow2.dropna(how="any")

    for i in range(len(df_arrow2)):


        plt.plot([df_arrow2['별도매출_22'].iloc[i], df_arrow2['별도매출_21'].iloc[i]],
                 [df_arrow2['별도영업이익_22'].iloc[i], df_arrow2['별도영업이익_21'].iloc[i]], color='black', alpha=0.2)


    df_arrow3 = df[['별도매출_22', '별도영업이익_22', '별도매출_23', '별도영업이익_23']]
    df_arrow3.dropna(how="any")

    for i in range(len(df_arrow3)):
        arrow = FancyArrowPatch((df_arrow3['별도매출_22'].iloc[i], df_arrow3['별도영업이익_22'].iloc[i]),
                                (df_arrow3['별도매출_23'].iloc[i], df_arrow3['별도영업이익_23'].iloc[i]),
                                arrowstyle='-|>', mutation_scale=15, color='black', alpha=0.5, lw=1, linestyle='--', )
        ax.add_patch(arrow)



    # x축, y축 설정
    xmin = plt.axis()[0]
    xmax = plt.axis()[1]
    ymin = plt.axis()[2]
    ymax = plt.axis()[3]

    # y_range 설정
    if ymin>=0:
        y_range = ymax
    else:
        y_range = ymax - ymin

    if xmin >= 0:
        plt.xlim(0, xmax*1.1)
    else:
        plt.xlim(xmin, xmax*1.1)

    #회사명 표시
    for i in range(len(df_2022)):
        plt.text(df_2022['별도매출_22'].iloc[i] - xmax*0.03, df_2022['별도영업이익_22'].iloc[i] + y_range*0.02,
                 df_2022['Name'].iloc[i])

    # 축, 범례 표시
    plt.xlabel('매출액', fontsize=17, labelpad=30)
    plt.ylabel('영업이익', fontsize=17, labelpad=45)
    plt.legend(['2023.반기 LTM','2022', '2021', '2020'], fontsize=15, loc='upper left')


    # 수평선(영업이익=0) 표시
    if xmin >= 0:
        plt.plot([0,xmax*1.1],[0,0], color='indianred', linestyle='--', linewidth=1.2, alpha=0.5)
    else:
        plt.plot([xmin, xmax*1.1], [0, 0], color='indianred', linestyle='--', linewidth=1.2, alpha=0.5)

    # HTML로 내보내기
    #graph = mpld3.fig_to_html(f, figid='THIS_IS_FIGID')
    graph = mpld3.fig_to_html(fig, figid='THIS_IS_FIGID')

    return graph