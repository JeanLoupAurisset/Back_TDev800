# Generated by Django 3.2.4 on 2021-06-25 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='album',
            fields=[
                ('id_album', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='device',
            fields=[
                ('id_device', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('marque', models.CharField(max_length=50)),
                ('modele', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='utilisateur',
            fields=[
                ('id_utilisateur', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('login', models.CharField(max_length=50)),
                ('mdp', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=50)),
                ('date_inscription', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='photo',
            fields=[
                ('id_photo', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('id_device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tdev800.device')),
                ('id_utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tdev800.utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='metadata',
            fields=[
                ('id_metadata', models.BigAutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('valeur', models.CharField(max_length=50)),
                ('mode_acquisition', models.CharField(max_length=50)),
                ('date_ajout', models.DateField()),
                ('id_photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tdev800.photo')),
            ],
        ),
        migrations.CreateModel(
            name='regrouper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tdev800.album')),
                ('id_photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tdev800.photo')),
            ],
            options={
                'unique_together': {('id_photo', 'id_album')},
            },
        ),
        migrations.CreateModel(
            name='posseder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ajout', models.DateField()),
                ('id_device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tdev800.device')),
                ('id_utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tdev800.utilisateur')),
            ],
            options={
                'unique_together': {('id_utilisateur', 'id_device')},
            },
        ),
    ]
