from django import forms
from pybo.models import Question, Answer, Document
import pandas as pd

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']

        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'uploadedFile']
        labels = {
            'title': '제목',
            'uploadedFile': '파일'
        }

class UploadFileForm(forms.Form):
    #name = forms.CharField(max_length = 15)
    # file = forms.FileField()
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,}))

class CompanyNameAll(forms.Form):
    df_회사명_List = pd.read_excel('static/회사명_List.xlsx')
    company_name_all = df_회사명_List['회사명'].tolist()

    taraget = forms.ChoiceField(choices=[(name, name) for name in company_name_all])