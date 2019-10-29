from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g, jsonify, abort

{route} = Blueprint('{route}', __name__)

@{route}.route('/{route}/')
def index():
	return render_template('{route}/{route}.html')
