from flask import Flask, render_template, request, jsonify, g

print("------------------asffffff------------------")
app = Flask(__name__)
print("------------------asffffff222222------------------")
@app.route('/')
def index():
	return("test data asdf")

if __name__ == '__main__':
	print("here i am")
	app.run(host='0.0.0.0', debug=True)
