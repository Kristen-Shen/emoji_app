from flask import Flask, render_template, request
import pandas as pd
import random 
from flask_paginate import Pagination, get_page_parameter
import hashlib

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main_page():
    # get the emoji dataset
    df = pd.read_csv("updated_emojis.csv")

    # search by keywords
    query = request.form.get("query", "")
    if query:
        # make search query case-insensitive 
        df = df[df['slug'].str.contains(query, case=False, na=False)]

    # Pagination 
    per_page = 30
    current_page = int(request.args.get('page', 1))
    start = (current_page - 1) * per_page
    end = current_page * per_page
    emojis = df.iloc[start:end].to_dict('records')

    # Pagination object
    pagination = Pagination(page=current_page, total=df.shape[0], per_page=per_page, css_framework='bootstrap4')

    return render_template("main.html", emojis=emojis, query=query, pagination=pagination)

@app.route("/emojis/<string:name>")
def emoji(name):
    df = pd.read_csv("updated_emojis.csv")
    matching_rows = df[df['slug'] == name]
    emoji = matching_rows.to_dict('records')[0] if not matching_rows.empty else None

    # Generate a unique color based on the 'slug' of each emoji
    def generate_color_from_slug(slug):
        hash_object = hashlib.md5(slug.encode())
        hex_color = '#' + hash_object.hexdigest()[:6]
        return hex_color

    background_color = generate_color_from_slug(name)

    return render_template("emoji2.html", emoji=emoji, background_color=background_color)

if __name__ == "__main__":
    app.run(debug=True)
