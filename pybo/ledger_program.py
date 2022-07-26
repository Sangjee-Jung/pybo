import pandas as pd
import numpy as np

def make_years(start_year, end_year):
    years = []
    for i in range(int(start_year), int(end_year)+1):
        years.append(i)

    return years

def ledger_table(excel_files, years):

    l = pd.read_excel(excel_files[0])

    lists = []
    for excel_file in excel_files:
        lists.append(pd.read_excel(excel_file, sheet_name = None))

    #기본설정 > 추후 Input으로 대체
    월계 = "  [ 월         계 ]"
    누계 = "  [ 누         계 ]"
    계정명행 = 1
    계정명열 = 6
    시작행 = 3


    head = l.loc[시작행 - 1].tolist()
    head_replaced = []
    for i in head:
        head_replaced.append(i.replace(" ", ""))

    #데이터프레임 생성
    df = pd.DataFrame(columns = head_replaced)
    df['년'] = ""
    df['계정명'] = ""

    #파일반복 > i
    for i in range(len(lists)):
        year = years[i]
        sheets = list(lists[i].keys())

        #파일 내 시트 반복 > j

        for j in range(len(sheets)):
            sheet = lists[i][sheets[j]]
            계정명 = sheets[j].split("_")[1]

            df_추가 = sheet.loc[3:, ]
            df_추가['년'] = year
            df_추가['계정명'] = 계정명
            df_추가.columns = df.columns.tolist()

            df = pd.concat([df, df_추가])

    df = df.reset_index(drop=True)

    index_월계 = df[df['적요란'] == 월계].index
    index_누계 = df[df['적요란'] == 누계].index

    df = df.drop(index_월계)
    df = df.drop(index_누계)

    df = df.reset_index(drop=True)


    월 = []
    for row in df['날짜']:
        월.append(float(str(row).split('-')[0]))
    df['월'] = 월

    col1 = df.columns[-2:-1].to_list()
    col2 = df.columns[-3:-2].to_list()
    col3 = df.columns[-1:].to_list()
    col4 = df.columns[:-3].to_list()
    new_col = col1 + col2 + col3 + col4
    df = df[new_col]

    df.to_excel("media/result/ledger.xlsx", index=False)

    return df