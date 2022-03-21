from flask import Flask, render_template,flash, redirect, url_for, session
from forms import Prefered
import requests
import json
app = Flask(__name__)

app.config["SECRET_KEY"] = "937d1b62d2a00fc76624e1db5c24ca78"

arg= requests.get("http://ec2-3-249-97-221.eu-west-1.compute.amazonaws.com/")
dictToSend = {"arguments":["a","b","c"], "attacks":["(a,b)","(b,c)"],"semantics":"grounded"}


@app.route('/')
def welcome():
    res = requests.post('http://ec2-3-249-97-221.eu-west-1.compute.amazonaws.com', json=dictToSend)
    res = res.json()
    reqs = json.loads(arg.content)
    return render_template('main.html', reqs=reqs, res=res)

@app.route('/custom', methods=["GET","POST"])
def prefered():
    form = Prefered()
    if form.validate_on_submit():
        flash(f'{form.attacks.data}',"success")

        #arg = list(form.arguments.data.split("-"))
        
        try:
            ata = str(form.attacks.data)
            ata=ata.replace(" ","")

            argu=ata.replace("->",";")

            ata = ata.replace("->",",")
            ata = ata.replace(";",");(")
            ata = "("+ata + ")"
            att = list(ata.split(";"))
            
            arg = list(argu.split(";"))
            arg = list(dict.fromkeys(argu))
            arg.remove(";")
            sem = form.semantics.data
            dictToSend = {"arguments":arg, "attacks":att,"semantics":sem}
            res = requests.post('http://ec2-3-249-97-221.eu-west-1.compute.amazonaws.com', json=dictToSend)
        except:
            dictToSend = {"arguments": "", "attacks":"","semantics":""}
            res = requests.post('http://ec2-3-249-97-221.eu-west-1.compute.amazonaws.com', json=dictToSend)

        
        tmp = res.json()
        print(arg) 
        session['res'] = res.json()
        try:
            lnt = len(tmp[sem])
            session["ln"] = list(range(0,lnt))
        except:
            session["ln"]= []

        if (form.semantics.data== "preferred"):
            return redirect(url_for("custpref"))

        if (form.semantics.data== "grounded"):
            return redirect(url_for("custg"))

        if (form.semantics.data== "stable"):
            return redirect(url_for("custs"))

        if (form.semantics.data== "semistable"):
            return redirect(url_for("custss"))

    return render_template('custom.html', form = form, title = "Custom")

@app.route('/preferred')
def custpref():
    form = Prefered()
    res = session.get('res', None)
    ln = session.get('ln', None)

    return render_template('Prefered.html', res=res, ln=ln)

@app.route('/grounded')
def custg():
    form = Prefered()
    res = session.get('res', None)


    return render_template('main.html', res=res)

@app.route('/stable')
def custs():
    form = Prefered()
    ln = session.get('ln', None)
    res = session.get('res', None)



    return render_template('stable.html', res=res, ln=ln)

@app.route('/semistable')
def custss():
    form = Prefered()
    ln = session.get('ln', None)
    res = session.get('res', None)


    return render_template('semi-stable.html', res=res, ln=ln)


if __name__ == '__main__':
    app.run(debug=True)