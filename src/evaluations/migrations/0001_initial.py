# Generated by Django 4.1.5 on 2023-01-06 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_name', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='WidgetLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('widget_xpath', models.CharField(max_length=255)),
                ('widget_type', models.CharField(choices=[('TextInput', 'TextInput'), ('SelectInput', 'SelectInput'), ('Anchor', 'Anchor'), ('Datepicker', 'Datepicker'), ('DateSelect', 'DateSelect'), ('RadioSet', 'RadioSet')], max_length=255)),
                ('widget_url', models.URLField(max_length=255)),
                ('micro_measures', models.JSONField()),
                ('user_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='widget_logs', to='evaluations.usersession')),
            ],
        ),
        migrations.AddField(
            model_name='usersession',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sessions', to='evaluations.version'),
        ),
    ]