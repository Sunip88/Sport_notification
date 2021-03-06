# Generated by Django 3.1 on 2021-02-19 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trigger', models.BooleanField(default=False)),
                ('external_id', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('week', 'Week'), ('day', 'Day'), ('live', 'Live')], max_length=32)),
                ('notification_route', models.CharField(choices=[('http', 'Http Request'), ('email', 'Email')], max_length=32)),
                ('sent', models.DateTimeField(null=True)),
                ('notification_url', models.TextField(blank=True, null=True)),
                ('notification_email', models.TextField(blank=True, null=True)),
                ('teams', models.ManyToManyField(to='data.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
                ('subscription_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.subscription')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=64)),
                ('competition_id', models.CharField(max_length=64)),
                ('league_id', models.CharField(max_length=64)),
                ('competition_name', models.CharField(max_length=128)),
                ('location', models.CharField(max_length=128)),
                ('scheduled', models.CharField(max_length=16)),
                ('ht_score', models.CharField(max_length=64, null=True)),
                ('ft_score', models.CharField(max_length=64, null=True)),
                ('et_score', models.CharField(max_length=64, null=True)),
                ('score', models.CharField(max_length=64, null=True)),
                ('time', models.CharField(max_length=32, null=True)),
                ('league_name', models.CharField(max_length=128, null=True)),
                ('last_changed', models.DateTimeField(null=True)),
                ('added', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=32)),
                ('team_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_team_one', to='data.team')),
                ('team_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_team_two', to='data.team')),
            ],
        ),
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=64)),
                ('competition_id', models.CharField(max_length=64)),
                ('competition_name', models.CharField(max_length=128)),
                ('league_id', models.CharField(max_length=64)),
                ('league_name', models.CharField(max_length=128, null=True)),
                ('location', models.CharField(max_length=128)),
                ('start_datetime', models.DateTimeField()),
                ('team_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixture_team_one', to='data.team')),
                ('team_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixture_team_two', to='data.team')),
            ],
        ),
    ]
