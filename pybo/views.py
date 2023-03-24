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
from .landscape import load_industry, define_industry, define_companies, make_scatter, make_df_customized, make_scatter_customized, make_df_개별
from .excel_programs import excel_concat
from .cf import make_df_cf_waterfall, make_graph_cf_waterfall
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
    df_회사명_List = pd.read_excel('static/회사명_List.xlsx')

    company_name_all = df_회사명_List['회사명'].tolist()
    company_code_all_가공전 = df_회사명_List['종목코드'].tolist()
    company_code_all = []
    for code in company_code_all_가공전:
        company_code_all.append(code[1:7])


    target = request.GET.get('target')
    분류기준 = request.GET.get('분류기준')

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

        df_산업코드_산업, df_산업코드_기업 = load_industry(분류기준)
        code_2, name_2, df_industry, code_4, name_4, code_3, name_3 = define_industry(target, df_산업코드_산업, df_산업코드_기업)


        #session 지정
        request.session["code_4"] = code_4
        request.session["target"] = target
        request.session["분류기준"] = 분류기준


    try:

        industry_lists = []
        for i in range(len(df_industry)):
            industry_lists.append(df_industry.iloc[i,].tolist())



        context = {"company_name_all": company_name_all, "target": target, "code_2": code_2, "name_2": name_2,
               "code_4": code_4, "name_4": name_4, "code_3": code_3, "name_3": name_3,
               "df_industry": df_industry.to_html(justify='center',
                                                  index=False, classes="table table-sm table-hover"),
               "industry_lists": industry_lists}

        return render(request, 'pybo/industry_landscape.html', context)

    except:
        context = {"company_name_all": company_name_all, "target": target, "code_2": code_2, "name_2": name_2, "code_4": code_4, "name_4": name_4, "code_3": code_3, "name_3": name_3, "df_industry": df_industry.to_html(justify='center',
                                                                                                index=False, classes="table table-sm table-hover")}

        return render(request, 'pybo/industry_landscape.html', context)

def industry_landscape_1_1(request):

    #회사명 list 생성
    df_회사명_List = pd.read_excel('static/회사명_List.xlsx')
    company_name_all = df_회사명_List['회사명'].tolist()

    context = {"company_name_all": company_name_all}

    return render(request, 'pybo/industry_landscape_1_1.html', context)

def industry_landscape_2(request):
    level = int(request.GET.get('level'))
    fs_type = request.GET.get('fs_type')

    code_4 = request.session["code_4"]
    target = request.session["target"]
    분류기준 = request.session["분류기준"]

    if 분류기준 == "한국표준":
        search_code = str(code_4)[0:level+1]
    else:
        search_code = str(code_4)[0:level*2]


    search_name, companies, df = define_companies(search_code, level, fs_type, 분류기준)


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

    request.session['fs_type'] = fs_type

    #리스트 만들기
    df_lists = []
    df2 = df.reset_index(drop =False)

    for i in range(len(df2)):
        df_lists.append(df2.iloc[i,].tolist())

    #Column명 변경
    df.columns = ["매출액_FY19", "매출액_FY20", "매출액_FY21", "매출액_FY22LTM",
                  "영업이익_FY19", "영업이익_FY20", "영업이익_FY21", "영업이익_FY22LTM", "영업이익률_FY22", "순위"]

    context = {"level": level, "code": search_code, "name": search_name, "companies": companies,
               "df": df.to_html(justify='center',index = True, classes="table table-sm",  float_format='{0:>,.0f}'.format ),
               "df_lists": df_lists,"fs_type": fs_type, "target": target, "df_index": df_index}

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

    #비교대상 필터링
    graph_대상 = request.GET.getlist('graph_대상')

    df_대상 = df[df['index'].isin(graph_대상)].reset_index(drop=True)
    df_대상.set_index('index')

    #Session 만들기
    request.session['graph_대상'] = graph_대상

    #그래프 그려
    graph = make_scatter(df_대상)

    context = {"graph": graph, "level": level, "code": search_code, "name": search_name, 'graph_대상':graph_대상}

    return render(request, 'pybo/industry_landscape_3.html', context)


def industry_landscape_3_2(request):
    target = request.GET.get('target')
    fs_type = request.GET.get('fs_type')

    #df 만들어
    df_개별 = make_df_개별(target, fs_type)



    df_개별 =df_개별.reset_index(drop=False)
    df_개별['index'] = [target]
    df_개별.set_index('index')


    #graph 그려
    graph = make_scatter(df_개별)

    # df Trim
    df_개별.drop(['순위'], axis=1, inplace=True)
    df_개별.drop(['index'], axis=1, inplace=True)


    context = {"df_개별": df_개별.to_html(justify='center', index = False, classes="table table-sm",  float_format='{0:>,.0f}'.format),
               "graph": graph, "target": target}

    return render(request, 'pybo/industry_landscape_3_2.html', context)


def industry_landscape_4(request):

    x축 = request.GET.get('x축')
    y축 = request.GET.get('y축')
    size = request.GET.get('size')
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')

    years = make_years(start_year, end_year)


    #Session 가져오기
    graph_대상 = request.session['graph_대상']
    fs_type = request.session['fs_type']

    #df 생성
    df_customized = make_df_customized(x축,y축,graph_대상, fs_type, size)

    #그래프 그려
    graph_customized, name_x축,name_y축 = make_scatter_customized(df_customized, x축, y축, size, years)


    if size == "n/a":
        df_customized.columns = [name_x축 + "_FY19", name_x축 + "_FY20", name_x축 + "_FY21", name_x축 + "_FY22LTM",
                                 name_y축 + "_FY19", name_y축 + "_FY20", name_y축 + "_FY21", name_y축 + "_FY22LTM"]
    else:
        df_customized.columns = [name_x축 + "_FY19", name_x축 + "_FY20", name_x축 + "_FY21", name_x축 + "_FY22LTM",
                                 name_y축 + "_FY19", name_y축 + "_FY20", name_y축 + "_FY21", name_y축 + "_FY22LTM",
                                 "size_FY19", "size_FY20", "size_FY21", "size_FY22LTM",]

    #기간 맞게 column 삭제
    df_customized_dropped = df_customized
    if 2019 in years:
        pass
    else:
        if size == "n/a":
            df_customized_dropped.drop([name_x축 + "_FY19",name_y축 + "_FY19" ], axis=1, inplace=True)
        else:
            df_customized_dropped.drop([name_x축 + "_FY19", name_y축 + "_FY19", "size_FY19" ], axis=1, inplace=True)

    if 2020 in years:
        pass
    else:
        if size == "n/a":
            df_customized_dropped.drop([name_x축 + "_FY20",name_y축 + "_FY20"], axis=1, inplace=True)
        else:
            df_customized_dropped.drop([name_x축 + "_FY20", name_y축 + "_FY20", "size_FY20"], axis=1, inplace=True)

    if 2021 in years:
        pass
    else:
        if size == "n/a":
            df_customized_dropped.drop([name_x축 + "_FY21",name_y축 + "_FY21"], axis=1, inplace=True)
        else:
            df_customized_dropped.drop([name_x축 + "_FY21", name_y축 + "_FY21", "size_FY21"], axis=1, inplace=True)

    if 2022 in years:
        pass
    else:
        if size == "n/a":
            df_customized_dropped.drop([name_x축 + "_FY22LTM",name_y축 + "_FY22LTM"], axis=1, inplace=True)
        else:
            df_customized_dropped.drop([name_x축 + "_FY22LTM", name_y축 + "_FY22LTM", "size_FY22LTM"], axis=1, inplace=True)


    context = {"df_customized_dropped": df_customized_dropped.to_html(justify='center',index = True, classes="table table-sm",  float_format='{0:>,.0f}'.format),
               "graph_customized": graph_customized, "years": years}


    return render(request, 'pybo/industry_landscape_4.html', context)


def industry_landscape_5(request):

    start_year_CF = request.GET.get('start_year_CF')
    end_year_CF = request.GET.get('end_year_CF')

    years = make_years(start_year_CF, end_year_CF)

    # Session 가져오기
    graph_대상 = request.session['graph_대상']
    fs_type = request.session['fs_type']

    # df 생성
    df_cf_waterfall = make_df_cf_waterfall(graph_대상, fs_type)

    # 그래프 그려
    graph_cf_waterfall, index = make_graph_cf_waterfall(df_cf_waterfall, graph_대상)

    context = {"df_cf_waterfall": df_cf_waterfall.to_html(justify='center',index = True, classes="table table-sm",  float_format='{0:>,.0f}'.format),
               "graph_cf_waterfall": graph_cf_waterfall, "index": index }

    return render(request, 'pybo/industry_landscape_5.html', context)

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

    try:
        excel_file_2022 = request.FILES["excel_file_2022"]
        excel_files.append(excel_file_2022)
        years.append(2022)
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




