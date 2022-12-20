# Generated by Django 4.0 on 2022-12-16 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_campagne_amount_needed'),
    ]

    operations = [
        migrations.AddField(
            model_name='campagne',
            name='debut_campagne',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='campagne',
            name='fin_campagne',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='investissement',
            name='telephone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Echeance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periode', models.DateField()),
                ('montant_investi', models.IntegerField(default=0)),
                ('interet', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('yes', 'Rembourser'), ('non', 'Non Rembourser')], default='non', max_length=100)),
                ('date_remboursement', models.DateTimeField(auto_now=True, verbose_name='dernier modification')),
                ('investissement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.campagne')),
            ],
        ),
    ]