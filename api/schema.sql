CREATE TABLE utilisateur(
   id_utilisateur INT,
   nom VARCHAR(50),
   login VARCHAR(50),
   mdp VARCHAR(50),
   email VARCHAR(50),
   date_inscription DATE,
   PRIMARY KEY(id_utilisateur)
);

CREATE TABLE device(
   id_device INT,
   nom VARCHAR(50),
   marque VARCHAR(50),
   modele VARCHAR(50),
   PRIMARY KEY(id_device)
);

CREATE TABLE album(
   id_album INT,
   nom VARCHAR(50),
   PRIMARY KEY(id_album)
);

CREATE TABLE photo(
   id_photo INT,
   nom VARCHAR(50),
   id_device INT NOT NULL,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_photo),
   FOREIGN KEY(id_device) REFERENCES device(id_device),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE metadata(
   id_metadata INT,
   type VARCHAR(50),
   valeur VARCHAR(50),
   mode_acquisition VARCHAR(50),
   date_ajout DATE,
   id_photo INT NOT NULL,
   PRIMARY KEY(id_metadata),
   FOREIGN KEY(id_photo) REFERENCES photo(id_photo)
);

CREATE TABLE regrouper(
   id_photo INT,
   id_album INT,
   PRIMARY KEY(id_photo, id_album),
   FOREIGN KEY(id_photo) REFERENCES photo(id_photo),
   FOREIGN KEY(id_album) REFERENCES album(id_album)
);

CREATE TABLE posseder(
   id_utilisateur INT,
   id_device INT,
   date_ajout DATE,
   PRIMARY KEY(id_utilisateur, id_device),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_device) REFERENCES device(id_device)
);
