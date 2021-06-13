from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_results = mongo.db.mars_app.find_one()
    return render_template("index.html", mars_results = mars_results)

@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_app
    mars_results = scrape_mars.scrape()
    mars_data.update({}, mars_results, upsert = True)
    return redirect("/", code = 302)


if __name__ == "__main__":
    app.run(debug = True)