#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask, request, render_template, flash, redirect, url_for
import numpy as np

#sys.path.append('./libs/')
from pizza_choice import main_choice

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'cat'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    image = request.files['image']
    if image.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if image and allowed_file(image.filename):
        filename = image.filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        return render_template('index.html', image_path=os.path.join('uploads', filename))
    else:
        flash('Invalid file type. Please upload a PNG, JPG, or JPEG image.')
        return redirect(request.url)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('upload_image'))

    return render_template('index.html', image_path='')


@app.route('/process_image', methods=['POST'])
def process_image():
    image_path = [request.form['image_path']]
    language_code = request.form['language_code']
    beurk = request.form['beurk']
    miam = request.form['miam']
    result = main_choice(image_path,
                         language_code,
                         beurk, miam)

    return render_template('result.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
