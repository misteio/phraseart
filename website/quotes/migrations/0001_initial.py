# Generated by Django 5.1 on 2024-08-13 19:15

import django.core.validators
import django.db.models.deletion
import imagekit.models.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=120, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('slug', models.SlugField(editable=False, max_length=120, unique=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='images/bio/')),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('original_name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='FileImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('file', models.ImageField(blank=True, upload_to='images/%Y/%m/%d/')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Missed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('original_name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('slug', models.SlugField(editable=False, max_length=100, unique=True)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(4)])),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('body', models.TextField()),
                ('analyze', models.TextField(blank=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('image_square', models.ImageField(blank=True, upload_to='images/generated/%Y/%m/%d/')),
                ('image_vertical', models.ImageField(blank=True, upload_to='images/generated/%Y/%m/%d/')),
                ('image_horizontal', models.ImageField(blank=True, upload_to='images/generated/%Y/%m/%d/')),
                ('explicit_text', models.BooleanField(default=False)),
                ('slider_selected', models.BooleanField(default=False)),
                ('featured_selected', models.BooleanField(default=False)),
                ('sub_slider_selected', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_quote', to='quotes.author')),
                ('file_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='file_image_quote', to='quotes.fileimage')),
                ('tags', models.ManyToManyField(to='quotes.tag')),
            ],
            options={
                'ordering': ('-title',),
            },
        ),
    ]
