from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#creation de la  base de données
database="todo"
password=quote_plus("root")
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:{}@localhost:5432/{}'.format(password,database)

app.config['SQLALCHEMY_DATABASE_URI'] = conn

# Ne pas avoir les avertissements
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# creation de l'instance de la BD
db = SQLAlchemy(app)

#creation de la table tache 

class Tache(db.Model):
    __tablename__ = 'tache'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),nullable = False)
    created_at= db.Column(db.DateTime,nullable = False,default=datetime.utcnow)
    def __repr__(self):
        return f"Todo {self.name}"
    
@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form['name']
        new_tache = Tache(name = name)
        try:
            db.session.add(new_tache)
            db.session.commit()
            return redirect("/")
        except Exception:
            return "une erreur s'est produite !!!"
    else:
        taches = Tache.query.order_by(Tache.created_at)
    return render_template("index.html", taches = taches)


# suppression des taches

@app.route("/delete/<int:id>/")
def delete(id):
    tache = Tache.query.get_or_404(id)
    try:
        db.session.delete(tache)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "Un problème est survenu lors de la suppression !"


@app.route("/update/<int:id>/", methods = ["GET", "POST"])
def update(id):
    tache = Tache.query.get_or_404(id)
    if request.method == "POST":
        tache.name = request.form["name"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception:
            return "Une erreur s'est produite lors de la mise à jour !"
    else:
        title = "Mise à jour"
        return render_template("update.html", title = title, tache = tache)
        


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
  