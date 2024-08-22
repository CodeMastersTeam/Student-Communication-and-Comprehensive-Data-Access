from Flask_links import locations
from app import Direct_links
from flask import Flask

app = Flask(__name__)

app.secret_key = "Gwapo"

Direct_links(app)
locations(app)





if __name__ == "__main__":
    app.run(debug = True)