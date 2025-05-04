#!/usr/bin/env python3
from waitress import serve
from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, redirect, url_for 
from db_access import DatabaseAccess
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret_key")  

ZAZNAMY_PER_PAGE = 10

@app.route('/zaznamy/<int:page>')
def zaznamy(page):

    sort_order = request.args.get('sort', 'desc')  
    start_date = request.args.get('start_date', '')  
    end_date = request.args.get('end_date', '')
    specified_user = request.args.get('user', '')
   
    pruchody = DatabaseAccess.GetPruchody(ZAZNAMY_PER_PAGE, page, sort_order, start_date, end_date,specified_user)

    return render_template('zaznamy.html',
                            zaznamy=pruchody,
                            page=page, pocet = ZAZNAMY_PER_PAGE,
                            sort_order = sort_order,
                            start_date = start_date,
                            end_date = end_date,
                            user = specified_user)

@app.route('/prezence/<int:page>')
def prezence(page):

    pruchody = DatabaseAccess.GetKartyUvnitr(ZAZNAMY_PER_PAGE, page)
    return render_template('prezence.html',
                            zaznamy=pruchody,
                            page=page, pocet = ZAZNAMY_PER_PAGE)

@app.route('/karty/<int:page>')   
def karty(page):
    message = request.args.get('message', '')

    karty = DatabaseAccess.GetKarty(ZAZNAMY_PER_PAGE, page)
    return render_template('karty.html',
                            karty=karty,
                            page=page,
                            pocet = ZAZNAMY_PER_PAGE,
                            message = message)

@app.route('/add_karta', methods=['POST'])
def add_karta():
    jmeno = request.form.get('jmeno')
    uid = request.form.get('uid')

    if jmeno and uid:
        success = DatabaseAccess.AddKarta(jmeno, uid)
        if success:
            flash('Karta přidána úspěšně!', 'success')
        else:
            flash('Chyba při přidávání karty.', 'error')
    else:
        flash('Neplatný vstup.', 'error')
    
    return redirect(url_for('karty', page=1))

@app.route('/edit_karta', methods=['POST'])
def edit_karta():
    jmeno = request.form.get('jmeno')
    uid = request.form.get('uid')
    valid = 'valid' in request.form

    page = request.args.get('page', 1, type=int)
    old_uid = request.args.get('old_uid')

    if jmeno and uid:

        success = DatabaseAccess.UpdateKarta(jmeno, uid, valid, old_uid)

        if success:
            flash('Karta byla úspěšně aktualizována!', 'success')
        else:
            flash('Chyba při aktualizaci karty.', 'error')
    else:
        flash('Neplatný vstup.', 'error')
    return redirect(url_for('karty', page=page))
                                
@app.route('/')
def main():
    return prezence(page=1)

if __name__ == "__main__":
    serve(app,host="0.0.0.0", port=8080)
