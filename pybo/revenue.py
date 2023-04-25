import mpld3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def make_df_revenue_product(graph_대상):

    df = pd.read_excel("static/KV_매출구성비_상장_개발용.xlsx", header=0, index_col='회사명_기준')
    df_revenue_product = df.loc[graph_대상]

    return df_revenue_product

def make_graph_revenue_product(df_revenue_product, graph_대상,years):

    # 색상설정
    kpmg_blue = '#00338D'
    medium_blue = '#005EB8'
    light_blue = '#0091DA'
    violet = '#483698'
    purple = '#470A68'
    light_purple = '#6D2077'
    green = '#00A3A1'
    gray = '#CCCCCC'

    colors_using = []

    # 그래프 설정
    f = plt.figure(figsize=(6 * len(years), 6 * len(graph_대상)))
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False
    plt.rc('font', size=13)


    wedgeprops = {'width': 0.4, 'edgecolor': 'w', 'linewidth': 0.5}

    for i, 대상 in enumerate(graph_대상):


        for y in range(len(years)):

            labels = []
            sizes = []
            누적 = 0

            # 3대매출 없는 경우
            if df_revenue_product.loc[대상][str(years[y]) + '_3대_제품명'] is np.nan:

                labels.append(df_revenue_product.loc[대상][str(years[y]) + '_1대_제품명'])
                labels.append(df_revenue_product.loc[대상][str(years[y]) + '_2대_제품명'])
                labels.append('기타')

                sizes.append(df_revenue_product.loc[대상][str(years[y]) + '_1대_구성비'])
                sizes.append(df_revenue_product.loc[대상][str(years[y]) + '_2대_구성비'])

                누적 = (df_revenue_product.loc[대상][str(years[y]) + '_1대_구성비'] + df_revenue_product.loc[대상][
                    str(years[y]) + '_2대_구성비'])
                sizes.append(100 - 누적)

                colors_using = [medium_blue, light_blue, gray]

            else:
                # 2대매출 없는 경우
                if df_revenue_product.loc[대상][str(years[y]) + '_2대_제품명'] is np.nan:

                    labels.append(df_revenue_product.loc[대상][str(years[y]) + '_1대_제품명'])
                    labels.append('기타')

                    sizes.append(df_revenue_product.loc[대상][str(years[y]) + '_1대_구성비'])

                    누적 = (df_revenue_product.loc[대상][str(years[y]) + '_1대_구성비'])
                    sizes.append(100 - 누적)

                    colors_using = [medium_blue, gray]

                #다 있을 경우
                else:
                    labels.append(df_revenue_product.loc[대상][ str(years[y]) +'_1대_제품명'])
                    labels.append(df_revenue_product.loc[대상][str(years[y]) + '_2대_제품명'])
                    labels.append(df_revenue_product.loc[대상][str(years[y]) + '_3대_제품명'])
                    labels.append('기타')

                    sizes.append(df_revenue_product.loc[대상][ str(years[y]) +'_1대_구성비'])
                    sizes.append(df_revenue_product.loc[대상][str(years[y]) + '_2대_구성비'])
                    sizes.append(df_revenue_product.loc[대상][str(years[y]) + '_3대_구성비'])

                    누적 = (df_revenue_product.loc[대상][ str(years[y]) +'_1대_구성비'] + df_revenue_product.loc[대상][str(years[y]) + '_2대_구성비'] + df_revenue_product.loc[대상][str(years[y]) + '_3대_구성비'])
                    sizes.append(100 - 누적)

                    colors_using = [medium_blue, light_blue, green, gray]

            # 그래프 그리기
            ax = plt.subplot(len(graph_대상), len(years), (i * len(years)) + (y + 1))
            ax.axis('off')

            try:
                ax.pie(sizes, autopct='%1.1f%%',startangle=90, counterclock=False, radius=0.65, labeldistance = 1.1, wedgeprops = wedgeprops, colors = colors_using,)
                ax.annotate("연결/별도", (0, 0), ha="center")
                ax.annotate("매출액 XXX", (0, -0.1), ha="center")

                plt.legend(labels, loc=(0.01,0.01), fontsize = 12)

                ax.set_title(대상 +"_" + str(years[y]) , fontsize=17)

            except:
                pass


    graph = mpld3.fig_to_html(f, figid='THIS_IS_FIGID')

    return graph
