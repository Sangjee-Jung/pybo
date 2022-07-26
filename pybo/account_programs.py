import pandas as pd
import numpy as np

def account_table(columns, rows, target_account):

    f_ledger = pd.DataFrame()
    for i in range(len(columns)):
        f_ledger[columns[i]] = rows[i]

    df_target = f_ledger.loc[f_ledger['계정명'] == target_account]

    return df_target

def client_analysis(df_target, target_account, account_type):

    #속성 설정
    증가 = ""
    감소 = ""

    if account_type == "자산" or account_type == "비용":
        증가 = "차변"
        감소 = "대변"
    elif account_type == "부채" or account_type == "수익":
        증가 = "대변"
        감소 = "차변"
    else:
        raise

    #index 생성
    client_codes = set(df_target['코드'].tolist())
    client_codes = [code for code in client_codes if np.isnan(code) == False]

    정렬 = []
    client_names = []
    for code in client_codes:
        정렬.append(df_target.loc[df_target['코드'] == code][증가].sum())
        client_names.append(df_target.loc[df_target['코드'] == code]['거래처'].tolist()[0])

    df_index = pd.DataFrame({'code': client_codes, 'name': client_names, '정렬': 정렬})
    df_index = df_index.sort_values(by='정렬', ascending=False)
    df_index = df_index.reset_index()
    del df_index['index']
    del df_index['정렬']

    #날짜 생성
    years = []
    months = []

    for year in df_target['년'].tolist():
        if year not in years:
            years.append(year)

    for month in range(1,13):
        months.append(month)

    df_증가_월 = df_index.copy()
    df_감소_월 = df_index.copy()
    df_증가_년 = df_index.copy()
    df_감소_년 = df_index.copy()

    # 월단위 증가
    for year in years:
        for month in months:
            year_month = str(year) + "-" + str(month)

            year_month_list_증가_월 = []

            for code in df_index['code']:
                year_month_list_증가_월.append(df_target.loc[(df_target['코드'] == code) & (df_target['년'] == year) & (
                            df_target['월'] == month), 증가].sum())

            df_증가_월[year_month] = year_month_list_증가_월

    # 월단위 감소
    for year in years:
        for month in months:
            year_month = str(year) + "-" + str(month)

            year_month_list_감소_월 = []

            for code in df_index['code']:
                year_month_list_감소_월.append(df_target.loc[(df_target['코드'] == code) & (df_target['년'] == year) & (
                            df_target['월'] == month), 감소].sum())

            df_감소_월[year_month] = year_month_list_감소_월

    # 연단위 증가
    for year in years:
        year_list_증가_년 = []

        for code in df_index['code']:
            year_list_증가_년.append(df_target.loc[(df_target['코드'] == code) & (df_target['년'] == year), 증가].sum())

        df_증가_년[year] = year_list_증가_년

    #연단위 감소
    for year in years:
        year_list_감소_년 = []

        for code in df_index['code']:
            year_list_감소_년.append(df_target.loc[(df_target['코드'] == code) & (df_target['년'] == year), 감소].sum())

        df_감소_년[year] = year_list_감소_년

    return df_증가_월, df_감소_월, df_증가_년, df_감소_년