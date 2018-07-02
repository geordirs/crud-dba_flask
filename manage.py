import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

# enlace a base de datos via sqlalchemy
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "estudiante.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# modelado
class Estudiante(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    lastname = db.Column(db.String(20), unique=True, nullable=False)
    #title = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Name: {},Lastname: {}>".format(self.name, self.lastname)

# vistas
# @app.route("/")
@app.route("/", methods=["GET", "POST"])
def home():
    # return "My flask app"
    if request.form:
        print(request.form)
        estudiante = Estudiante(name=request.form.get("name"), lastname=request.form.get("lastname"))
        #lastname = Estudiante(lastname=request.form.get("lastname"))
        db.session.add(estudiante)
        db.session.commit()
    
    estudiantes = Estudiante.query.all()
    return render_template("home.html", estudiantes=estudiantes)
    # return render_template("home.html")
    
@app.route("/update", methods=["POST"])
def update():
    newname = request.form.get("nombre")
    newlastname = request.form.get("apellido")
    idestudiante = request.form.get("idestudiante")
    estudiante = Estudiante.query.get(idestudiante)
    estudiante.name = newname
    estudiante.lastname = newlastname
    db.session.commit()
    return redirect("/")  

@app.route("/delete", methods=["POST"])
def delete():
    idestudiante = request.form.get("idestudiante")
    estudiante = Estudiante.query.get(idestudiante)
    db.session.delete(estudiante)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)



