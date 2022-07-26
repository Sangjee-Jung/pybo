from django import forms
from pybo.models import Question, Answer, Document

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
    # name = forms.CharField(max_length = 15)
    # files = forms.FileField()
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))