#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash, session, g
import pymysql.cursors

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

'''
def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="ahaddou2",
            password="mdp",
            database="BDD_ahaddou2",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        activate_db_options(g.db)
    return g.db
'''

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="root",
            password="password",
            database="MaBaseDeDonnees",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        activate_db_options(g.db)
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def activate_db_options(db):
    cursor = db.cursor()
    cursor.execute("SHOW VARIABLES LIKE 'sql_mode'")
    result = cursor.fetchone()
    if result:
        modes = result['Value'].split(',')
        if 'ONLY_FULL_GROUP_BY' not in modes:
            cursor.execute("SET sql_mode=(SELECT CONCAT(@@sql_mode, ',ONLY_FULL_GROUP_BY'))")
            db.commit()
    cursor.execute("SHOW VARIABLES LIKE 'lower_case_table_names'")
    result = cursor.fetchone()
    if result and result['Value'] != '0':
        cursor.execute("SET GLOBAL lower_case_table_names = 0")
        db.commit()
    cursor.close()


@app.route('/', methods=['GET'])
def show_layout():
    return render_template('layout.html')


@app.route('/genre-film/show', methods=['GET'])
def show_genre():
    mycursor = get_db().cursor()
    if mycursor is None:
        flash("Erreur de connexion à la base de données", 'alert-danger')
        return redirect('/')
    sql = '''SELECT id, libelleGenre, logo FROM genresFilms'''
    mycursor.execute(sql)
    genresFilms = mycursor.fetchall()
    mycursor.close()

    return render_template('genre/show_genre.html', genresFilms=genresFilms)


@app.route('/genre-film/add', methods=['GET'])
def add_genre():
    return render_template('genre/add_genre.html')

@app.route('/genre-film/add', methods=['POST'])
def valid_add_genre():
    print("Ajout d'un nouveau genre de film")
    libelleGenre = request.form.get('libelleGenre') or None
    logo = request.form.get('logo') or None

    message = f"Genre ajouté avec succès ! Libellé : {libelleGenre} | Logo : {logo}"
    flash(message)

    sql = '''INSERT INTO genresFilms (libelleGenre, logo) 
             VALUES (%s, %s)'''
    tuple_param = (libelleGenre, logo)

    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    mycursor.close()

    return redirect('/genre-film/show')


@app.route('/genre-film/delete', methods=['GET'])
def delete_genre():
    id = request.args.get('id', '')
    if not id:
        flash("ID du genre manquant", 'alert-danger')
        return redirect('/genre-film/show')

    mycursor = get_db().cursor()
    sql = "DELETE FROM genresFilms WHERE id = %s"
    mycursor.execute(sql, (id,))
    get_db().commit()
    mycursor.close()

    flash("Genre de film supprimé avec succès, ainsi que tous les films associés", 'alert-success')
    return redirect('/genre-film/show')


@app.route('/genre-film/edit', methods=['GET'])
def edit_genre():
    mycursor = get_db().cursor()
    if mycursor is None:
        flash("Erreur de connexion à la base de données", 'alert-danger')
        return redirect('/genre-film/show')

    id = request.args.get('id', '')
    if not id:
        flash("ID du genre manquant", 'alert-danger')
        return redirect('/genre-film/show')
    sql = "SELECT id, libelleGenre, logo FROM genresFilms WHERE id = %s"
    mycursor.execute(sql, (id,))
    genresFilms = mycursor.fetchone()
    mycursor.close()

    if not genresFilms:
        flash("Genre introuvable", 'alert-danger')
        return redirect('/genre-film/show')

    return render_template('genre/edit_genre.html', genresFilms=genresFilms)



@app.route('/genre-film/edit', methods=['POST'])
def valid_edit_genre():
    id = request.form.get('id')
    libelleGenre = request.form.get('libelleGenre') or None
    logo = request.form.get('logo') or None

    message = f"Genre mis à jour avec succès ! Libellé : {libelleGenre} | Logo : {logo}"
    flash(message)

    sql = '''UPDATE genresFilms 
             SET libelleGenre = %s, logo = %s 
             WHERE id = %s;'''
    tuple_param = (libelleGenre, logo, id)

    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    mycursor.close()

    return redirect('/genre-film/show')


@app.route('/film/show', methods=['GET'])
def show_film():
    mycursor = get_db().cursor()
    if mycursor is None:
        flash("Erreur de connexion à la base de données", 'alert-danger')
        return redirect('/')
    sql = '''
    SELECT films.id, films.titreFilm, films.dateSortie, films.nomRealisateur, films.duree, films.affiche,
           genresFilms.libelleGenre, films.genre_id 
    FROM films 
    JOIN genresFilms ON films.genre_id = genresFilms.id
    '''
    mycursor.execute(sql)
    films = mycursor.fetchall()
    mycursor.close()

    return render_template('film/show_film.html', films=films)

    sql = '''
    SELECT films.id, films.titreFilm, films.dateSortie, films.nomRealisateur, films.duree, films.affiche,
           genresFilms.libelleGenre 
    FROM films 
    JOIN genresFilms ON films.genre_id = genresFilms.id
    '''
    mycursor.execute(sql)
    films = mycursor.fetchall()
    mycursor.close()

    return render_template('film/show_film.html', films=films)


@app.route('/film/add', methods=['GET'])
def add_film():
    mycursor = get_db().cursor()
    sql = "SELECT id, libelleGenre FROM genresFilms"
    mycursor.execute(sql)
    genresFilms = mycursor.fetchall()
    print(genresFilms)
    return render_template('film/add_film.html', genresFilms=genresFilms)



@app.route('/film/add', methods=['POST'])
def valid_add_film():
    mycursor = get_db().cursor()
    titreFilm = request.form.get('titreFilm', '')
    dateSortie = request.form.get('dateSortie', '')
    nomRealisateur = request.form.get('nomRealisateur', '')
    genre_id = request.form.get('genre_id', '')
    duree = request.form.get('duree', '')
    affiche = request.form.get('affiche', '')
    sql = '''INSERT INTO films (titreFilm, dateSortie, nomRealisateur, genre_id, duree, affiche)
             VALUES (%s, %s, %s, %s, %s, %s)'''
    mycursor.execute(sql, (titreFilm, dateSortie, nomRealisateur, genre_id, duree, affiche))
    get_db().commit()
    flash(f"Film ajouté : {titreFilm}", 'alert-success')
    return redirect('/film/show')


@app.route('/film/delete', methods=['GET'])
def delete_film():
    mycursor = get_db().cursor()
    id = request.args.get('id', '')
    sql = "DELETE FROM films WHERE id = %s"
    mycursor.execute(sql, (id,))
    get_db().commit()
    flash(f"Un film supprimé, id : {id}", 'alert-warning')
    return redirect('/film/show')


@app.route('/film/edit', methods=['GET'])
def edit_film():
    print("Affichage du formulaire d'édition pour le film")
    id = request.args.get('id', '')
    if not id:
        flash("ID du film manquant", 'alert-danger')
        return redirect('/film/show')

    mycursor = get_db().cursor()
    sql = "SELECT id, titreFilm, genre_id, duree, dateSortie, nomRealisateur, affiche FROM films WHERE id = %s"
    mycursor.execute(sql, (id,))
    films = mycursor.fetchone()

    if not films:
        flash("Film introuvable", 'alert-danger')
        return redirect('/film/show')
    sql_genres = "SELECT id, libelleGenre FROM genresFilms"
    mycursor.execute(sql_genres)
    genresFilms = mycursor.fetchall()

    mycursor.close()

    print(f"Données du film récupérées : {films}")
    print(f"Genres de films récupérés : {genresFilms}")

    return render_template('film/edit_film.html', films=films, genresFilms=genresFilms)


@app.route('/film/edit', methods=['POST'])
def valid_edit_film():
    print('Modification du film dans le tableau')
    id = request.form.get('id')
    titreFilm = request.form.get('titreFilm') or None
    dateSortie = request.form.get('dateSortie') or None
    nomRealisateur = request.form.get('nomRealisateur') or None
    genre_id = request.form.get('genre_id') or None
    duree = request.form.get('duree') or None
    affiche = request.form.get('affiche') or None

    message = f"Film mis à jour avec succès ! Titre : {titreFilm} | Date de sortie : {dateSortie} | Réalisateur : {nomRealisateur} | Genre ID : {genre_id} | Durée : {duree} minutes | Affiche : {affiche}"
    flash(message)

    sql = '''UPDATE films 
             SET titreFilm = %s, dateSortie = %s, nomRealisateur = %s, genre_id = %s, duree = %s, affiche = %s 
             WHERE id = %s;'''
    tuple_param = (titreFilm, dateSortie, nomRealisateur, genre_id, duree, affiche, id)

    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_param)
    get_db().commit()

    return redirect('/film/show')


@app.route('/film/filtre', methods=['GET'])
def filtre_film():
    mycursor = get_db().cursor()
    if mycursor is None:
        flash("Erreur de connexion à la base de données", 'alert-danger')
        return redirect('/film/show')
    sql_genres = "SELECT id, libelleGenre FROM genresFilms"
    mycursor.execute(sql_genres)
    genresFilms = mycursor.fetchall()

    filter_word = request.args.get('filter_word', '')
    genre_id = request.args.get('genre_id', '')
    duree_min = request.args.get('duree_min', '')
    duree_max = request.args.get('duree_max', '')

    sql = "SELECT films.id, films.titreFilm, films.dateSortie, films.nomRealisateur, films.duree, films.affiche, genresFilms.libelleGenre FROM films JOIN genresFilms ON films.genre_id = genresFilms.id WHERE 1=1"
    sql_params = []

    if filter_word:
        sql += " AND films.titreFilm LIKE %s"
        sql_params.append(f"%{filter_word}%")

    if genre_id:
        sql += " AND films.genre_id = %s"
        sql_params.append(genre_id)

    if duree_min:
        sql += " AND films.duree >= %s"
        sql_params.append(duree_min)

    if duree_max:
        sql += " AND films.duree <= %s"
        sql_params.append(duree_max)

    mycursor.execute(sql, sql_params)
    films = mycursor.fetchall()
    mycursor.close()

    return render_template('film/filtre_film.html', films=films, genresFilms=genresFilms)


if __name__ == '__main__':
    app.run(debug=True)
