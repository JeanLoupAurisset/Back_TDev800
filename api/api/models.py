from django.db import models

class utilisateur(models.Model):
    id_utilisateur = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    mdp = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    date_inscription = models.DateField()

class device(models.Model):
    id_device = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=50)
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)

class album(models.Model):
    id_album = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=50)

class photo(models.Model):
    id_photo = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=50)
    id_device = models.ForeignKey(device, on_delete=models.CASCADE)
    id_utilisateur = models.ForeignKey(utilisateur, on_delete=models.CASCADE)

class metadata(models.Model):
    id_metadata = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=50)
    valeur = models.CharField(max_length=50)
    mode_acquisition = models.CharField(max_length=50)
    date_ajout = models.DateField()
    id_photo = models.ForeignKey(photo, on_delete=models.CASCADE)

class regrouper(models.Model):
    id_photo = models.ForeignKey(photo, on_delete=models.CASCADE, primary_key=True)
    id_album = models.ForeignKey(album, on_delete=models.CASCADE, primary_key=True)

class posseder(models.Model):
    id_utilisateur = models.ForeignKey(utilisateur, on_delete=models.CASCADE, primary_key=True)
    id_device = models.ForeignKey(device, on_delete=models.CASCADE, primary_key=True)
    date_ajout = models.DateField()