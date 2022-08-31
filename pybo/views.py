from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from django.http import HttpResponseNotAllowed, HttpResponse, FileResponse
from .forms import QuestionForm, AnswerForm, UploadFileForm
import matplotlib.pyplot as plt
from .ledger_program import make_years, ledger_table
from .account_programs import account_table, client_analysis
from .models import Document, Dart_is_2
import os
from django.core.files.storage import FileSystemStorage
import pandas as pd
from .landscape import load_industry, define_industry, define_companies, make_scatter
from .excel_programs import excel_concat
import mpld3

import logging
logger = logging.getLogger('pybo')

def index(request):
    logger.info("INFO 레벨로 출력")
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list':question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

def industry_landscape(request):
    df_산업코드_산업, df_산업코드_기업, company_name_all, company_code_all = load_industry()
    target = request.GET.get('target')
    code_2 = None
    name_2 = None
    code_4 = None
    name_4 = None
    code_3 = None
    name_3 = None

    df_industry = pd.DataFrame()

    if target == None:
        pass
    else:
        code_2, name_2, df_industry, code_4, name_4, code_3, name_3 = define_industry(target, df_산업코드_산업, df_산업코드_기업)

        #session 지정
        request.session["code_4"] = code_4

    try:
        df_industry_2 = {}
        df_industry_2['Lv'] = df_industry['Lv'].tolist()
        df_industry_2['CODE'] = df_industry['CODE'].tolist()

        context = {"company_name_all": company_name_all, "target": target, "code_2": code_2, "name_2": name_2,
               "code_4": code_4, "name_4": name_4, "code_3": code_3, "name_3": name_3,
               "df_industry": df_industry.to_html(justify='center',
                                                  index=False, classes="table table-sm table-hover"),
               "df_industry_2": df_industry_2}

        return render(request, 'pybo/industry_landscape.html', context)

    except:
        context = {"company_name_all": company_name_all, "target": target, "code_2": code_2, "name_2": name_2, "code_4": code_4, "name_4": name_4, "code_3": code_3, "name_3": name_3, "df_industry": df_industry.to_html(justify='center',
                                                                                                index=False, classes="table table-sm table-hover")}

        return render(request, 'pybo/industry_landscape.html', context)

def industry_landscape_2(request):
    level = int(request.GET.get('level'))
    fs_type = request.GET.get('fs_type')

    code_4 = request.session["code_4"]
    search_code = str(code_4)[0:level+1]

    #dart_is = Dart_is_2.objects.all().values()
    #df_dart_is = pd.DataFrame(dart_is)


    search_name, companies, df = define_companies(search_code, level, fs_type)

    #Session 만들기
    df_columns = df.columns.tolist()
    df_rows = []
    for df_column in df_columns:
        df_rows.append(df[df_column].tolist())
    df_index = df.index.tolist()

    request.session['df_columns'] = df_columns
    request.session['df_rows'] = df_rows
    request.session['df_index'] = df_index

    request.session['level'] = level
    request.session['search_code'] = search_code
    request.session['search_name'] = search_name


    context = {"level": level, "code": search_code, "name": search_name, "companies": companies, "df": df.to_html(justify='center',index = True, classes="table table-sm",  float_format='{0:>,.0f}'.format ),"fs_type": fs_type}

    return render(request, 'pybo/industry_landscape_2.html', context)

def industry_landscape_3(request):
    #Session 가져오기
    df_columns = request.session['df_columns']
    df_rows = request.session['df_rows']
    df_index = request.session['df_index']

    level = request.session['level']
    search_code = request.session['search_code']
    search_name = request.session['search_name']

    #df 생성
    df = pd.DataFrame()
    for i in range(len(df_columns)):
        df[df_columns[i]] = df_rows[i]
    df['index'] = df_index
    df.set_index('index')

    graph = make_scatter(df)

    context = {"graph": graph, "level": level, "code": search_code, "name": search_name}

    return render(request, 'pybo/industry_landscape_3.html', context)

def industry_landscape_4(request):

    number = int(request.GET.get('number'))

    # Session 가져오기
    df_columns = request.session['df_columns']
    df_rows = request.session['df_rows']
    df_index = request.session['df_index']

    # df 생성
    df = pd.DataFrame()
    df.index = df_index
    for i in range(len(df_columns)):
        df[df_columns[i]] = df_rows[i]
    df['index'] = df_index
    df.set_index('index')

    df_상위 = None
    df_하위 = None

    df_상위 = df.iloc[0:number,:]
    df_하위 = df.iloc[number:,:]

    graph_상위 = make_scatter(df_상위)
    graph_하위 = make_scatter(df_하위)


    context = {"number": number, "graph_상위": graph_상위, "graph_하위":graph_하위}

    return render(request, 'pybo/industry_landscape_4.html', context)


def ledger(request):
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')

    years = []

    if start_year == None or end_year == None:
        pass
    else:
        years = make_years(start_year, end_year)

    context = {'years': years}
    return render(request, 'pybo/ledger.html', context)

def upload(request):

    excel_files = []
    years = []

    try:
        excel_file_2017 = request.FILES["excel_file_2017"]
        excel_files.append(excel_file_2017)
        years.append(2017)
    except:
        pass

    try:
        excel_file_2018 = request.FILES["excel_file_2018"]
        excel_files.append(excel_file_2018)
        years.append(2018)
    except:
        pass

    try:
        excel_file_2019 = request.FILES["excel_file_2019"]
        excel_files.append(excel_file_2019)
        years.append(2019)
    except:
        pass

    try:
        excel_file_2020 = request.FILES["excel_file_2020"]
        excel_files.append(excel_file_2020)
        years.append(2020)
    except:
        pass

    try:
        excel_file_2021 = request.FILES["excel_file_2021"]
        excel_files.append(excel_file_2021)
        years.append(2021)
    except:
        pass

    table = ledger_table(excel_files, years)

    context = {"table": table.to_html(justify='center',
                                      max_rows=30,
                                      index=False,
                                      na_rep="",
                                      float_format='{0:>,.0f}'.format,
                                      show_dimensions=True,
                                      classes="table table-sm table-bordered")}


    return render(request,'pybo/upload.html', context)

def account(request):

    accounts = []
    target_account = ""
    account_type = ""
    df = ""


    if request.method == "POST":
        excel_file_ledger = (request.FILES["excel_file_ledger"])
        f_ledger = pd.read_excel(excel_file_ledger)

        # DataFrame 뿌수기
        columns = f_ledger.columns.tolist()
        rows = []
        for column in columns:
            rows.append(f_ledger[column].tolist())

        #Session 지정
        request.session['columns'] = columns
        request.session['rows'] = rows


        for account in f_ledger['계정명'].tolist():
            if account not in accounts:
                accounts.append(account)

    context = {"accounts" : accounts}


    return render(request,'pybo/account.html', context)

def account_target(request):
    target_account = request.GET.get('target_account')
    account_type = request.GET.get('account_type')

    # Session 지정
    request.session['target_account'] = target_account
    request.session['account_type'] = account_type

    # Session 가져오기
    columns = request.session['columns']
    rows = request.session['rows']

    df_target = account_table(columns, rows, target_account)


    context = {"target_account" : target_account,
               "account_type": account_type,
               "df_target": df_target.to_html(justify='center',
                                      max_rows=30,
                                      index=False,
                                      na_rep="",
                                      float_format='{0:>,.0f}'.format,
                                      show_dimensions=True, classes="table table-sm table-bordered")
               }

    return render(request,'pybo/account_target.html', context)

def account_result(request):

    # Session 가져오기
    columns = request.session['columns']
    rows = request.session['rows']
    target_account = request.session['target_account']
    account_type = request.session['account_type']

    #테이블 생성
    df_target = account_table(columns, rows, target_account)

    #거래처 분석
    df_증가_월, df_감소_월, df_증가_년, df_감소_년 = client_analysis(df_target, target_account, account_type)

    df1 = df_증가_년
    df2 = df_증가_월


    context = {"target_account": target_account,
               "account_type" : account_type,
               "df1": df1.to_html(justify='center',
                                  max_rows=20,
                                  index=False,
                                  float_format='{0:>,.0f}'.format,
                                  classes="table table-sm",
                                  ),
               "df2": df2.to_html(justify='center',
                                  max_rows=20,
                                  index=False,
                                  float_format='{0:>,.0f}'.format,
                                  classes="table table-sm",
                                  ),
               }

    return render(request, 'pybo/account_result.html', context)

def excel_settings(request):

    df_excel_기준 = None

    if request.method == "POST":
        excel_기준 = (request.FILES["excel_기준"])
        df_excel_기준 = pd.read_excel(excel_기준, header=None)

        # DataFrame 뿌수기
        columns = df_excel_기준.columns.tolist()
        rows = []
        for column in columns:
            rows.append(df_excel_기준[column].tolist())

        # Session 지정
        request.session['df_excel_기준_columns'] = columns
        request.session['df_excel_기준_rows'] = rows

        context = {"df_excel_기준": df_excel_기준.to_html(max_rows=30, classes="table table-sm table-bordered")}



        return render(request, 'pybo/excel_settings.html', context)

    else:

        return render(request, 'pybo/excel_settings.html', {"df_excel_기준": df_excel_기준})

def excel_settings_2(request):
    header_index = int(request.GET.get('header_index'))

    # Session 지정
    request.session['df_excel_기준_header_index'] = header_index

    # Session 가져오기
    columns = request.session['df_excel_기준_columns']
    rows = request.session['df_excel_기준_rows']

    # 테이블 생성

    df_excel_기준 = pd.DataFrame()
    for i in range(len(columns)):
        df_excel_기준[columns[i]] = rows[i]

    new_columns = df_excel_기준.loc[header_index].tolist()
    df_excel_기준 = df_excel_기준.loc[header_index+1:]
    df_excel_기준.columns = new_columns
    df_excel_기준 = df_excel_기준.reset_index(drop=True)

    # Session 지정
    request.session['new_columns'] = new_columns

    context = {"df_excel_기준": df_excel_기준.to_html(justify='center', max_rows=30, classes="table table-sm table-bordered")}

    return render(request, 'pybo/excel_settings_2.html', context)


def excel(request):
    selected = request.GET.getlist("selected")
    file_lists = []
    filename_lists = []
    header_index = int(request.session['df_excel_기준_header_index'])
    new_columns = request.session['new_columns']


    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            for count, x in enumerate(request.FILES.getlist("files")):
                file_lists.append(x)
                filename_lists.append(x.name)

            concated_df = excel_concat(file_lists, header_index, new_columns, filename_lists, selected)

            context = {'form': form, "concated_df": concated_df.to_html( max_rows=30, classes="table table-sm table-bordered"),}
            return render(request, 'pybo/excel.html', context)
    else:
        form = UploadFileForm()

    return render(request, 'pybo/excel.html', {'form': form,})


def downloadFile(request):
    file_path = os.path.abspath("media/result/")
    file_name = os.path.basename("media/result/ledger.xlsx")
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'),
                            content_type = 'application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="원장가공.xlsx"'

    return response

def excel_download(request):
    file_path = os.path.abspath("media/result/")
    file_name = os.path.basename("media/result/concated_excel.xlsx")
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'),
                            content_type = 'application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="합치기 완료.xlsx"'

    return response

def account_download(request):
    file_path = os.path.abspath("media/result/")
    file_name = os.path.basename("media/result/account.xlsx")
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'),
                            content_type = 'application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="계정분석.xlsx"'

    return response




