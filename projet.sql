DROP TABLE IF EXISTS genresFilms;
DROP TABLE IF EXISTS films;

CREATE TABLE genresFilms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    libelleGenre VARCHAR(255) NOT NULL,
    logo VARCHAR(255)
);

CREATE TABLE films (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titreFilm VARCHAR(255) NOT NULL,
    dateSortie DATE,
    nomRealisateur VARCHAR(255),
    genre_id INT,
    duree INT,
    affiche VARCHAR(255),
    FOREIGN KEY (genre_id) REFERENCES genresFilms(id) ON DELETE CASCADE
);


INSERT INTO films (titreFilm, dateSortie, nomRealisateur, genre_id, duree, affiche)
VALUES ('Le diner de con', '1998-04-15', 'Francis Veber', 1, 90, 'film_1.jpg'),
       ('Intouchable', '2012-03-28', 'Eric Toledano', 1, 125, 'film_2.jpg'),
       ('Piège de cristal', '1988-09-21', 'John McTiernan', 3, 90, 'film_3.jpg'),
       ('Indiana Jones', '1989-10-18', 'Steven Spielberg', 2, 125, 'film_4.jpg'),
       ('Blade Runner', '1982-09-15', 'Ridley Scott', 2, 145, 'film_5.jpg'),
       ('Alien', '1979-09-12', 'Ridley Scott', 2, 125, 'film_6.jpg'),
       ('L Exorciste', '2001-03-14', 'William Friedkin', 6, 90, 'film_7.jpg'),
       ('Psychose', '1960-11-02', 'Alfred Hitchcock', 6, 125, 'film_8.jpg'),
       ('Toy Story', '1996-03-27', 'John Lasseter', 5, 90, 'film_9.jpg'),
       ('Shrek', '2001-07-04', 'Andrew Adamson', 5, 90, 'film_10.jpg'),
       ('La Communauté de l anneau', '2001-12-19', 'Peter Jackson', 4, 150, 'film_11.jpg'),
       ('Les Deux Tours', '2002-12-18', 'Peter Jackson', 4, 152, 'film_12.jpg'),
       ('Le Retour du roi', '2003-12-17', 'Peter Jackson', 4, 149, 'film_13.jpg'),
       ('Inception', '2010-07-08', 'Christopher Nolan', 2, 90, 'film_14.jpg'),
       ('Warrior', '2011-09-14', 'Gavin O Connor', 3, 120, 'film_15.jpg'),
       ('Harry Potter à l école des sorciers', '2001-12-05', 'Chris Columbus', 4, 125, 'film_16.jpg'),
       ('Harry Potter et la Chambre des secrets', '2002-12-04', 'Chris Columbus', 4, 125, 'film_17.jpg'),
       ('Harry Potter et le Prisonnier d Azkaban', '2004-06-02', 'Alfonso Cuarón', 4, 125, 'film_18.jpg'),
       ('Harry Potter et la Coupe de feu', '2005-11-30', 'Mike Newell', 4, 125, 'film_19.jpg'),
       ('Harry Potter et l Ordre du phénix', '2009-07-15', 'David Yates', 4, 125, 'film_20.jpg');

INSERT INTO genresFilms (libelleGenre, logo)
VALUES ('Comedie', 'logo_comedie.png'),
       ('Science-Fiction', 'logo_science_fiction.png'),
       ('Action', 'logo_action.png'),
       ('Fantasy', 'logo_fantasy.png'),
       ('Animation', 'logo_animation.png'),
       ('Horreur', 'logo_horreur.png');
