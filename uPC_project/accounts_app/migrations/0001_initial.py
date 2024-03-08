# Generated by Django 5.0.1 on 2024-03-07 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('products_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='아이디')),
                ('password', models.CharField(max_length=128, verbose_name='비밀번호')),
                ('name', models.CharField(max_length=8, null=True, verbose_name='이름')),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='이메일')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='가입일')),
                ('auth', models.CharField(max_length=10, null=True, verbose_name='인증번호')),
                ('groups', models.ManyToManyField(blank=True, related_name='user_accounts', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_accounts', to='auth.permission')),
                ('whishlist', models.ManyToManyField(blank=True, related_name='wishlist', to='products_app.product')),
            ],
            options={
                'verbose_name': '사용자',
                'verbose_name_plural': '사용자',
                'db_table': '회원목록',
            },
        ),
    ]
