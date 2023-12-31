# Generated by Django 4.2.4 on 2023-08-21 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smtp_server', models.CharField(blank=True, max_length=255)),
                ('smtp_port', models.PositiveIntegerField(blank=True, null=True)),
                ('incoming_server', models.CharField(blank=True, max_length=255)),
                ('incoming_port', models.PositiveIntegerField(blank=True, null=True)),
                ('incoming_type', models.CharField(blank=True, choices=[('POP', 'POP'), ('IMAP', 'IMAP'), ('Local', 'Local')], max_length=10)),
                ('incoming_ssl', models.BooleanField(default=False)),
                ('incoming_tls', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='extenduser',
            name='app_password',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extenduser',
            name='email_conf',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ExtendUser', to='authentication.emailconfiguration'),
        ),
    ]
