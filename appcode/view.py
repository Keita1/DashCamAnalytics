__author__ = 'aub3'
#!/usr/bin/env python
from flask import render_template, redirect, request, abort,jsonify
import base64

def home():
    payload = {'gae_mode':False}
    return render_template('editor.html',payload = payload)


def add_views(app):
    app.add_url_rule('/',view_func=home)


