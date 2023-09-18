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

'''
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
        db_table = 'dart_is_2'
'''

class KvTotalCompanyInfo(models.Model):
    kis = models.TextField(db_column='KIS', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    stock = models.TextField(db_column='Stock', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    market_category = models.TextField(db_column='Market_category', blank=True, null=True)  # Field name made lowercase.
    market_category_revised = models.TextField(db_column='Market_category_revised', blank=True, null=True)  # Field name made lowercase.
    industry_code = models.TextField(db_column='Industry_code', blank=True, null=True)  # Field name made lowercase.
    industry_code_revised = models.IntegerField(db_column='Industry_code_revised', blank=True, null=True)  # Field name made lowercase.
    industry_name = models.TextField(db_column='Industry_name', blank=True, null=True)  # Field name made lowercase.
    industry_category = models.TextField(db_column='Industry_category', blank=True, null=True)  # Field name made lowercase.
    group = models.TextField(db_column='Group', blank=True, null=True)  # Field name made lowercase.
    ceo = models.TextField(db_column='CEO', blank=True, null=True)  # Field name made lowercase.
    establishment_date = models.TextField(db_column='Establishment_date', blank=True, null=True)  # Field name made lowercase.
    listing_date = models.TextField(db_column='Listing_date', blank=True, null=True)  # Field name made lowercase.
    company_size = models.TextField(db_column='Company_size', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    website = models.TextField(db_column='Website', blank=True, null=True)  # Field name made lowercase.
    main_products = models.TextField(db_column='Main_products', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KV_total_company_info'