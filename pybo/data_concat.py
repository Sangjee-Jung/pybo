import os
from django import template
from django.utils.html import format_html
import pandas as pd
import re

register = template.Library()

def handle_uploaded_file(f):
    with open(os.path.join('media/data_concat/', f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def delete_files_in_directory(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except:
            pass


def make_concated_dataset(head_index_start, head_index_end, selected_name_option, sheet_대상):

    #Header 설정
    header_range = []
    for i in range(head_index_start, head_index_end + 1):
        header_range.append(i)

    # 전체 파일 불러오기
    directory = "media/data_concat/"
    files = os.listdir(directory)

    filtered_sheets = []

    # 파일반복
    for file in files:
        all_sheets = pd.read_excel("media/data_concat/" + file, sheet_name=None, header=header_range)

        # 시트 반복
        for sheet_name, sheet_data in all_sheets.items():

            #전체시트일 경우(sheet_대상 == None) 또는 시트가 'sheet_대상'에 포함된 경우 함수 실행
            if len(sheet_대상) == 0 or sheet_name + " (File: " + file + ")" in sheet_대상:

                target_data = sheet_data.iloc[head_index_end:, ]

                # 시트명 추가
                if "시트명" in selected_name_option:
                    target_data.insert(0, '시트명', sheet_name)

                # 파일명 추가
                if "파일명" in selected_name_option:
                    target_data.insert(0, '파일명', file[:-5])

                filtered_sheets.append(target_data)
            else:
                pass


    # 합치기
    concated_data = pd.concat(filtered_sheets, ignore_index=True)
    concated_data.reset_index(drop=True)

    # 엑셀 저장
    concated_data.to_excel("media/result/dataset.xlsx")

    return concated_data


def make_concated_dataset_여러행(head_index_start, head_index_end, selected_name_option, sheet_대상, 여러행_시작행, 여러행_종료행):

    p = re.compile("[.]\d")

    # Header 설정
    header_range = []
    if head_index_start == 여러행_시작행:
        pass
    else:
        for i in range(head_index_start, 여러행_시작행):
            header_range.append(i)

    # 여러행 범위 설정
    여러행_range = []
    for i in range(여러행_시작행,여러행_종료행+1):
        여러행_range.append(i)


    # 전체 파일 불러오기
    directory = "media/data_concat/"
    files = os.listdir(directory)

    filtered_sheets = []

    # 파일반복
    for file in files:

        #최초 Header 설정
        if header_range == []:
            all_sheets = pd.read_excel("media/data_concat/" + file, sheet_name=None, header=None)
        else:
            all_sheets = pd.read_excel("media/data_concat/" + file, sheet_name=None, header=header_range)

        # 시트 반복
        for sheet_name, sheet_data in all_sheets.items():

            # 전체시트일 경우(sheet_대상 == None) 또는 시트가 'sheet_대상'에 포함된 경우 함수 실행
            if len(sheet_대상) == 0 or sheet_name + " (File: " + file + ")" in sheet_대상:

                target_data = sheet_data.iloc[여러행_시작행-len(header_range):, ]

                #n줄씩 ","로 합쳐
                df_grouped = target_data.groupby(target_data.index // len(여러행_range)).agg(lambda x: ', '.join(map(str, x)))
                df_grouped.reset_index(drop=True)

                #","기준 찢어
                df_splited = pd.DataFrame()

                if len(여러행_range) == 1:
                    for i in range(len(df_grouped.columns)):
                        df_splited[[i]] = df_grouped[df_grouped.columns[i]].str.split(',', expand=True)
                elif len(여러행_range) == 2:
                    for i in range(len(df_grouped.columns)):
                        df_splited[[i * 2, i * 2 + 1]] = df_grouped[df_grouped.columns[i]].str.split(',', expand=True)
                elif len(여러행_range) == 3:
                    for i in range(len(df_grouped.columns)):
                        df_splited[[i * 3, i * 3 + 1, i * 3 + 2]] = df_grouped[df_grouped.columns[i]].str.split(',', expand=True)
                elif len(여러행_range) == 4:
                    for i in range(len(df_grouped.columns)):
                        df_splited[[i * 4, i * 4 + 1, i * 4 + 2, i * 4 + 3]] = df_grouped[df_grouped.columns[i]].str.split(',', expand=True)
                elif len(여러행_range) == 5:
                    for i in range(len(df_grouped.columns)):
                        df_splited[[i * 5, i * 5 + 1, i * 5 + 2, i * 5 + 3, i * 5 + 4]] = df_grouped[df_grouped.columns[i]].str.split(',', expand=True)
                else:
                    df_splited = df_grouped

                # Hedaer 재설정
                df_grouped_columns_repeated = df_grouped.columns.repeat(len(여러행_range))

                #if len(여러행_range) == 3:
                #    new_cols = pd.MultiIndex.from_tuples([(p.sub("", col[0]), p.sub("", col[1]), df_splited.iloc[0][i]) for i, col in enumerate(df_grouped_columns_repeated)])

                if len(header_range) == 0:
                    new_cols = df_grouped_columns_repeated
                if len(header_range) == 1:
                    new_cols = pd.MultiIndex.from_tuples([(p.sub("", col),df_splited.iloc[0][i]+"."+str(i)) for i, col in enumerate(df_grouped_columns_repeated)])
                elif len(header_range) == 2:
                    new_cols = pd.MultiIndex.from_tuples([(p.sub("", col[0]),p.sub("", col[1]), df_splited.iloc[0][i]+"."+str(i)) for i, col in enumerate(df_grouped_columns_repeated)])
                elif len(header_range) == 3:
                    new_cols = pd.MultiIndex.from_tuples([(p.sub("", col[0]),p.sub("", col[1]),p.sub("", col[2]),df_splited.iloc[0][i]+"."+str(i)) for i, col in enumerate(df_grouped_columns_repeated)])
                elif len(header_range) == 4:
                    new_cols = pd.MultiIndex.from_tuples([(p.sub("", col[0]),p.sub("", col[1]),p.sub("", col[2]),p.sub("", col[3]),df_splited.iloc[0][i]+"."+str(i)) for i, col in enumerate(df_grouped_columns_repeated)])

                # Final 등장
                df_final = df_splited.drop(index=0)
                df_final.columns = new_cols

                # 시트명 추가
                if "시트명" in selected_name_option:
                    df_final.insert(0, '시트명', sheet_name)

                # 파일명 추가
                if "파일명" in selected_name_option:
                    df_final.insert(0, '파일명', file[:-5])

                filtered_sheets.append(df_final)
            else:
                pass

    # 합치기
    concated_data = pd.concat(filtered_sheets, ignore_index=True)
    concated_data.reset_index(drop=True)

    # 엑셀 저장
    concated_data.to_excel("media/result/dataset.xlsx")

    return concated_data


@register.simple_tag
def select_dataframe_columns(df):
    # Convert the DataFrame to an HTML table
    html_table = df.to_html(index=False)

    # Define the select element and embed the HTML table
    options = ''.join([f'<option value="{col}">{col}</option>' for col in df.columns])
    html_content = format_html(f'''
        <select id="columns">
            <option value=""></option>
            {options}
        </select>
        {html_table}
        <script>
            $(document).ready(function() {{
                $('#columns').change(function() {{
                    var selected_column = $(this).val();
                    var selected_values = [];
                    $('td:first-child').each(function() {{
                        if ($(this).text() == selected_column) {{
                            selected_values.push($(this).next().text());
                        }}
                    }});
                    console.log(selected_values);
                }});
            }});
        </script>
        ''')

    return html_content
