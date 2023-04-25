from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('industry-landscape/', views.industry_landscape, name='industry_landscape'),
    path('industry-landscape/1_1', views.industry_landscape_1_1, name='industry_landscape_1_1'),
    path('industry-landscape/2', views.industry_landscape_2, name='industry_landscape_2'),
    path('industry-landscape/3', views.industry_landscape_3, name='industry_landscape_3'),
    path('industry-landscape/3_2', views.industry_landscape_3_2, name='industry_landscape_3_2'),
    path('industry-landscape/4', views.industry_landscape_4, name='industry_landscape_4'),
    path('industry-landscape/4_2', views.industry_landscape_4_2, name='industry_landscape_4_2'),
    path('industry-landscape/5', views.industry_landscape_5, name='industry_landscape_5'),
    path('industry-landscape/5_2', views.industry_landscape_5_2, name='industry_landscape_5_2'),
    path('industry-landscape/6', views.industry_landscape_6, name='industry_landscape_6'),

    path('ledger/', views.ledger, name='ledger'),
    path('excel/', views.excel, name='excel'),
    path('excel/settings', views.excel_settings, name='excel_settings'),
    path('data/concat', views.data_concat, name='data_concat'),
    path('data/concat/2', views.data_concat_2, name='data_concat_2'),
    path('data/concat/2_2', views.data_concat_2_2, name='data_concat_2_2'),
    path('data/concat/3', views.data_concat_3, name='data_concat_3'),
    path('data/concat/download', views.data_concat_download, name='data_concat_download'),
    path('excel/settings/2', views.excel_settings_2, name='excel_settings_2'),
    path('excel/download', views.excel_download, name='excel_download'),
    path('account/download', views.account_download, name='account_download'),
    path('download/', views.downloadFile, name='downloadFile'),
    path('upload/', views.upload, name='upload'),
    path('account/', views.account, name='account'),
    path('account/target', views.account_target, name='account_target'),
    path('account/result', views.account_result, name='account_result'),
    path('excel/settings', views.excel_settings, name='excel_settings'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )