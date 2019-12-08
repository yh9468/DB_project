# Generated by Django 2.2.5 on 2019-12-08 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phonenum', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('data_useage', models.TextField()),
                ('message_useage', models.PositiveIntegerField(default=0, verbose_name='message_useage')),
                ('call_useage', models.PositiveIntegerField(default=0, verbose_name='call_useage')),
                ('User_contents', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': '유저',
                'verbose_name_plural': '유저들',
                'db_table': 'User_table',
            },
        ),
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('Agency_name', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('Agency_phone', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Agency_table',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('Plan_cost', models.PositiveIntegerField(verbose_name='Plan_cost')),
                ('Plan_name', models.CharField(max_length=50)),
                ('Plan_ID', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='Plan_ID')),
                ('Call_Limit', models.PositiveIntegerField(verbose_name='Call_Limit')),
                ('Message_Limit', models.PositiveIntegerField(verbose_name='Message_Limit')),
                ('Agency_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Agency')),
            ],
            options={
                'verbose_name': '요금제',
                'verbose_name_plural': '요금제들',
                'db_table': 'Plan_table',
            },
        ),
        migrations.CreateModel(
            name='INF_details',
            fields=[
                ('plan_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.Plan')),
                ('Month_limit', models.FloatField(verbose_name='Month_limit')),
                ('Day_limit', models.FloatField(verbose_name='Day_limit')),
            ],
            options={
                'db_table': 'INF_table',
            },
            bases=('app.plan',),
        ),
        migrations.CreateModel(
            name='NOR_details',
            fields=[
                ('plan_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.Plan')),
                ('Total_limit', models.FloatField(verbose_name='Total_limit')),
            ],
            options={
                'db_table': 'NOR_table',
            },
            bases=('app.plan',),
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('Family_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Family_id')),
                ('Family_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('agency_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Agency')),
            ],
            options={
                'verbose_name': '가족',
                'verbose_name_plural': '가족들',
                'db_table': 'Family_table',
            },
        ),
        migrations.AddField(
            model_name='myuser',
            name='Plan_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Plan'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
