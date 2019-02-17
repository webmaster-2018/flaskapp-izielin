from flask import g
from modele import *
from views import *
import os

# konfiguracja aplikacji
app.config.update(dict(
    SECRET_KEY='bardzosekretnawartosc',
))


@app.before_request
def before_request():
    g.db = baza
    g.db.connect(reuse_if_open=True)


@app.after_request
def after_request(response):
    g.db.close()
    return response

if __name__ == '__main__':
    app.run(debug=True)
