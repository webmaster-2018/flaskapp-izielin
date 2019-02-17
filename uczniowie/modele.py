#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  modele.py

from peewee import *

baza_plik = 'students.db'
baza = SqliteDatabase(baza_plik)  # instancja bazy

### MODELE #
class BazaModel(Model):
    class Meta:
        database = baza

class Gender(BazaModel):
    gender_name = CharField(null=False)

class MarkValue(BazaModel):
    values = IntegerField(null=False)

class Subject(BazaModel):
    subject_name = CharField(null=False)

class Class(BazaModel):
    class_name = TextField(null=False)
    rok_naboru = DateField()
    rok_matury = DateField()

class Student(BazaModel):
    student_name = CharField(null=False)
    surname = CharField(null=False)
    gender_key = ForeignKeyField(Gender)
    class_key = ForeignKeyField(Class)

class Mark(BazaModel):
    value = IntegerField(null=False)
    student_key = ForeignKeyField(Student, field='id', related_name='student_key')
    subject_key = ForeignKeyField(
        Subject, field='id', related_name='subject_key')
