import os
from django import template
from django.utils.html import format_html
import pandas as pd

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
