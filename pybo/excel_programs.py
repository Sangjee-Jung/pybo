import pandas as pd


def excel_concat(file_lists, header_index, new_columns, filename_lists, selected):

    df_lists = []
    for file in file_lists:
        df_lists.append(pd.read_excel(file, sheet_name = None))

    # 데이터프레임 생성
    df = pd.DataFrame(columns = new_columns)

    # 데이터프레임 열추가 옵션
    if "시트명" in selected:
        df["시트명"] = ""
    if "파일명" in selected:
        df["파일명"] = ""

    # 파일반복 > i
    for i in range(len(df_lists)):
        sheets = list(df_lists[i].keys())

        # 파일 내 시트 반복 > j
        for j in range(len(sheets)):
            sheet = df_lists[i][sheets[j]]

            df_추가 = sheet.loc[header_index+1:, ]

            # 데이터프레임 열추가 옵션
            if "시트명" in selected:
                df_추가["시트명"] = sheets[j]
            if "파일명" in selected:
                df_추가["파일명"] = filename_lists[i].split(".xlsx")[0]

            df_추가.columns = df.columns.tolist()
            df = pd.concat([df, df_추가])

    df = df.reset_index(drop=True)

    df.to_excel("media/result/concated_excel.xlsx", index=False)

    return df