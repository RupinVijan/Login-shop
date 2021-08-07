from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///log.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class log(db.Model):
    sno = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(50) )
    password = db.Column(db.String(50) )

    def __repr__(self) -> str:
        return f"{self.sno} - {self.username}"

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login" ,  methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if username=="Rupin" and password=="password":
            return redirect("/info")
        else :
            entry=log(username=username,password=password)
            db.session.add(entry)
            db.session.commit()
            return render_template("login.html")    
            

    return render_template("login.html")

@app.route("/logout")
def logout():
    
    return redirect("/login")

@app.route("/delete/<string:sno>" , methods=['GET','POST'])
def delete(sno):
    dets=log.query.filter_by(sno=sno).first()
    db.session.delete(dets)
    db.session.commit()
    return redirect("/login")

@app.route("/info",methods=['GET','POST'])
def info():
    dets=log.query.all()
    return render_template("info.html",dets=dets)


if __name__=="__main__":
    app.run(debug=True)