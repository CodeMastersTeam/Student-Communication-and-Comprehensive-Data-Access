from Flask_links import locations
from app import Direct_links
from flask import Flask, render_template, request

app = Flask(__name__)

Direct_links(app)
locations(app)




if __name__ == "__main__":
    app.run(debug = True)