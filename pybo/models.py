from django.db import models

# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

class Document(models.Model):
    title = models.CharField(max_length=200)
    uploadedFile = models.FileField(upload_to ="result/")
    dateTimeOfUpload = models.DateTimeField(auto_now=True)


class Dart_is_2(models.Model):
    id = models.IntegerField(primary_key=True)
    재무제표종류 = models.TextField()
    종목코드 = models.TextField()
    회사명 = models.TextField()
    시장구분 = models.TextField()
    업종 = models.TextField()
    업종명 = models.IntegerField()
    결산월 = models.IntegerField()
    항목코드 = models.TextField()
    항목명 = models.TextField()
    당기 = models.IntegerField(blank=True, null=True)
    전기 = models.IntegerField(blank=True, null=True)
    전전기 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        #db_table = 'dart_is_2'