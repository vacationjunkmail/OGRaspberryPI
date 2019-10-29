from flask import Flask, jsonify, render_template, request, g, session, flash, redirect,url_for

from routes.{route} import {route}

app = Flask(__name__)

app.register_blueprint({route})

if __name__ == "__main__":
	app.run(host = '0.0.0.0', debug = True)
