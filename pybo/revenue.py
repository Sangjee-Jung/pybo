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

            종류 = df_revenue_product.loc[대상][str(years[y]) + '_종류']

            try:
                매출액 = int(df_revenue_product.loc[대상][str(years[y]) + '_매출액']) / 1000000
            except:
                매출액 = ""

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

            #annotation 옵션
            threshold = 5 ## 상한선 비율
            count = 0

            try:
                #ax.pie(sizes, autopct='%1.1f%%',startangle=90, counterclock=False, radius=0.65, labeldistance = 1.1, wedgeprops = wedgeprops, colors = colors_using,)
                ax.pie(sizes,startangle=90, counterclock=False, radius=0.65, labeldistance = 1.1, wedgeprops = wedgeprops, colors = colors_using,)
                ax.annotate(종류 + " 매출", (0, 0), ha="center")
                ax.annotate(f'{매출액:,.0f}', (0, -0.1), ha="center")
                ax.annotate('(단위: KRW m)', (0.9, 0.7), ha="right")

                plt.legend(labels, loc=(0.01,0.01), fontsize = 12)

                ax.set_title(대상 +"_" + str(years[y]) , fontsize=17)
                ax.axis('off')

                ## annotation 설정

                for k in range(len(sizes)):
                    ang1, ang2 = ax.patches[k].theta1, ax.patches[k].theta2
                    center, r = ax.patches[k].center, ax.patches[k].r
                    text = f'{sizes[k]:.1f}%'

                    if sizes[k] < 0.1:
                        pass
                    else:
                        if sizes[k] < threshold:
                            count += 1

                            x축 = (r / 1.5 + count*0.1) * np.cos(np.pi / 180 * ((ang1 + ang2) / 2)) + center[0]
                            y축 = (r / 1.5 + count*0.1) * np.sin(np.pi / 180 * ((ang1 + ang2) / 2)) + center[1]
                            ax.text(x축, y축, text, ha='center', va='center', fontsize=13)

                        else:
                            x축 = (r / 1.5) * np.cos(np.pi / 180 * ((ang1 + ang2) / 2)) + center[0]
                            y축 = (r / 1.5) * np.sin(np.pi / 180 * ((ang1 + ang2) / 2)) + center[1]
                            ax.text(x축, y축, text, ha='center', va='center', fontsize=13)

            except:
                ax.set_title(대상 + "_" + str(years[y]), fontsize=17)
                #italic(fontstyle='italic') 적용이 안되는데 이유를 모르겠다.
                ax.text(0.5, 0.5, "Not Available", fontsize = 20, ha="center")
                ax.axis("off")


    graph = mpld3.fig_to_html(f, figid='THIS_IS_FIGID')

    return graph
