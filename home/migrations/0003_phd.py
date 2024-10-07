# Generated by Django 4.0 on 2024-09-16 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_colab_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PHD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('image', models.ImageField(upload_to='images/')),
                ('desig', models.TextField()),
                ('interest', models.TextField()),
                ('subject', models.TextField()),
                ('mail', models.EmailField(max_length=254)),
                ('github', models.URLField()),
                ('twitter', models.URLField()),
                ('linkedin', models.URLField()),
            ],
        ),
    ]