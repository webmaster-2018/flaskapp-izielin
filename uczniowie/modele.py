#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  modele.py

from peewee import *
import logging
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

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

# query = (Student
#          .select(Student.student_name, Student.surname)
#          .join_from(Student, Gender)  # Join Student -> Gender.
#          .join_from(Student, Class, JOIN.LEFT_OUTER))  # Join Student -> Class.
        #  .select(Student.content, fn.COUNT(Favorite.id).alias('count'))
        #  .where(User.username == 'huey')
        #  .group_by(Student.content))
