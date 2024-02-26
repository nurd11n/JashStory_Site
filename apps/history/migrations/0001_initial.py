# Generated by Django 4.2.5 on 2024-02-23 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('slug', models.SlugField(blank=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('name_ru', models.CharField(max_length=100, null=True, unique=True)),
                ('name_en', models.CharField(max_length=100, null=True, unique=True)),
                ('name_ky', models.CharField(max_length=100, null=True, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Years',
            fields=[
                ('slug', models.SlugField(blank=True, primary_key=True, serialize=False)),
                ('ages', models.DateField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('title_ru', models.CharField(max_length=100, null=True)),
                ('title_en', models.CharField(max_length=100, null=True)),
                ('title_ky', models.CharField(max_length=100, null=True)),
                ('article', models.TextField()),
                ('article_ru', models.TextField(null=True)),
                ('article_en', models.TextField(null=True)),
                ('article_ky', models.TextField(null=True)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='history.category')),
                ('category_en', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='history.category')),
                ('category_ky', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='history.category')),
                ('category_ru', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='history.category')),
                ('years', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='history.years')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('slug', models.SlugField(blank=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('title_ru', models.CharField(max_length=100, null=True, unique=True)),
                ('title_en', models.CharField(max_length=100, null=True, unique=True)),
                ('title_ky', models.CharField(max_length=100, null=True, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('posts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection', to='history.post')),
                ('posts_en', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='collection', to='history.post')),
                ('posts_ky', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='collection', to='history.post')),
                ('posts_ru', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='collection', to='history.post')),
            ],
        ),
    ]