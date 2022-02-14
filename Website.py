from flask import Flask, render_template
import requests
import json
app = Flask(__name__)


arg= requests.get("http://ec2-3-249-97-221.eu-west-1.compute.amazonaws.com/")

@app.route('/')
def welcome():

    reqs = json.loads(arg.content)
    return render_template('main.html', reqs=reqs)

if __name__ == '__main__':
    app.run(debug=True)