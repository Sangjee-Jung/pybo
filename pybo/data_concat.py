import os
from django import template
from django.utils.html import format_html

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
