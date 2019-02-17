#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, BooleanField
from wtforms import SelectField, FormField, FieldList
from wtforms.validators import Required

blad_1 = 'To pole jest wymagane'

class DodajForm(FlaskForm):
    student_name = StringField('Imie: ', validators=[
                          Required(message="blad_1")])
    surname = StringField('Nazwisko: ', validators=[
                          Required(message="blad_1")])
    gender = SelectField('Płec: ', coerce=int)
    klasa = SelectField('Klasa: ', coerce=int)

    id = HiddenField()

class DodajKlasaForm(FlaskForm):
    class_name = StringField('Nazwę klasy: ', validators=[
                          Required(message="blad_1")])
    rok_naboru = StringField('Rok naboru: ', validators=[
                          Required(message="blad_1")])
    rok_matury = StringField('Rok matury: ', validators=[
                          Required(message="blad_1")])


class DodajPrzedmiotForm(FlaskForm):
    subject_name = StringField('Nazwę przedmiotu: ', validators=[
        Required(message="blad_1")])

    id = HiddenField()


class DodajOceneForm(FlaskForm):
    value = SelectField('Ocena: ', coerce=int)
    student_key = SelectField('Nazwisko ucznia: ', coerce=int)
    subject_key = SelectField('Przedmiot: ', coerce=int)

    id = HiddenField()
