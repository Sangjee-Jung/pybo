# Generated by Django 4.0.3 on 2022-07-20 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0003_document_datetimeofupload'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dart_is',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dart_재무제표종류', models.TextField()),
                ('dart_종목코드', models.TextField()),
                ('dart_회사명', models.TextField()),
                ('dart_시장구분', models.TextField()),
                ('dart_업종', models.TextField()),
                ('dart_업종명', models.IntegerField()),
                ('dart_결산월', models.IntegerField()),
                ('dart_항목코드', models.TextField()),
                ('dart_항목명', models.TextField()),
                ('dart_당기', models.IntegerField(blank=True, null=True)),
                ('dart_전기', models.IntegerField(blank=True, null=True)),
                ('dart_전전기', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'dart_is',
                'managed': False,
            },
        ),
    ]
