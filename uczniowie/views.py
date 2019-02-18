#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template, request, flash, redirect, url_for, abort
from modele import *
from forms import *

app = Flask(__name__)

# widok domyślny


@app.route("/")
def index():
    return render_template('index.html')

def flash_errors(form):
    """Odczytanie wszystkich błędów formularza
    i przygotowanie komunikatów"""
    for field, errors in form.errors.items():
        for error in errors:
            if type(error) is list:
                error = error[0]
            flash("Błąd: {}. Pole: {}".format(
                error,
                getattr(form, field).label.text))


@app.route("/lista")
def lista():
    # students = Student.select()
    students = (Student
         .select(Student.id, Student.student_name, Student.surname, Gender.gender_name, Class.class_name)
         .join_from(Student, Gender)  # Join Student -> Gender.
         .join_from(Student, Class, JOIN.LEFT_OUTER))  # Join Student -> Class.
    # debug print
    for row in students:
        print(row.id, row.student_name, row.surname, row.gender_key.gender_name, row.class_key.class_name)
    return render_template('lista_wszystkich.html', students=students)


@app.route("/lista_klas")
def lista_klas():
    classes = Class.select()
    return render_template('lista_klas.html', classes=classes)


@app.route("/lista_klas/<id>")
def klasa(id):
    students = Student.select().where(Student.class_key == id)
    return render_template('lista.html', students=students, klasa=klasa)


@app.route("/lista_przedmiotow")
def lista_przedmiotow():
    subjects = Subject.select()
    return render_template('lista_przedmiotow.html', subjects=subjects)


@app.route("/lista_ocen/<id>")
# @app.route("/lista_klas/lista_ocen/<id>")
def lista_ocen(id):
    # marks = Mark.select().where(Mark.student_key == id)
    marks = (Mark.select(Mark.value, Student.id, Student.student_name, Student.surname, Subject.subject_name)
        .join_from(Mark, Student)
        .join_from(Mark, Subject, JOIN.LEFT_OUTER)
        .where(Student.id == id))

    return render_template('lista_ocen.html', marks=marks)


@app.route("/dodaj_ocene/<id>", methods=['GET', 'POST'])
# @app.route("/lista_klas/lista_ocen/dodaj_ocene/<id>", methods=['GET', 'POST'])
def dodaj_ocene(id):
    
    form = DodajOceneForm()
    form.value.choices = [(v.id, v.values)
                           for v in MarkValue.select()]
    form.student_key.choices = [
        (s.id, s.surname) for s in Student.select().where(Student.id == id)]
    form.subject_key.choices = [(s.id, s.subject_name)
                           for s in Subject.select()]

    if form.validate_on_submit():
        m = Mark(value=form.value.data,
                 student_key=form.student_key.data,
                 subject_key=form.subject_key.data)
        m.save()

        flash("Dodano ocene: {} ".format(
            form.value.data))
        return redirect(url_for('lista')) # FIXME lista_ocen(id)

    return render_template('dodaj_ocene.html', form=form)


@app.route("/dodaj", methods=['GET', 'POST'])
def dodaj():

    form = DodajForm()
    form.klasa.choices = [(c.id, c.class_name)
                          for c in Class.select()]
    form.gender.choices = [(g.id, g.gender_name)
                           for g in Gender.select()]

    if form.validate_on_submit():
        s = Student(student_name=form.student_name.data,
                    surname=form.surname.data,
                    gender_key=form.gender.data,
                    class_key=form.klasa.data)
        s.save()

        flash("Dodano ucznia: {} {}".format(
            form.student_name.data, form.surname.data))
        return redirect(url_for('lista'))

    return render_template('dodaj.html', form=form)

@app.route("/dodaj_klasy", methods=['GET', 'POST'])
def dodaj_klasy():

    form = DodajKlasaForm()

    if form.validate_on_submit():
        c = Class(class_name=form.class_name.data,
                  rok_naboru=form.rok_naboru.data,
                  rok_matury=form.rok_matury.data
        )
        c.save()

        flash("Dodano klasę: {}".format(
            form.class_name.data))
        return redirect(url_for('lista_klas'))

    return render_template('dodaj_klasy.html', form=form)


@app.route("/dodaj_przedmiot", methods=['GET', 'POST'])
def dodaj_przedmiot():

    form = DodajPrzedmiotForm()

    if form.validate_on_submit():
        s = Subject(subject_name=form.subject_name.data
        )
        s.save()

        flash("Dodano przedmiot: {}".format(
            form.subject_name.data))
        return redirect(url_for('dodaj_przedmiot'))

    return render_template('dodaj_przedmiot.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def get_or_404(id):
    try:
        s = Student.get_by_id(id)
        return s
    except Student.DoesNotExist:
        abort(404)
