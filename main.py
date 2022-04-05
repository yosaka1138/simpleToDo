import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# sqlの設定
app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text())
    status = db.Column(db.Integer)


db.create_all()


@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
@app.post("/add")
def add():
    task = Task()
    task.text = request.form["new_text"]
    if task.text == "":
        return redirect(url_for("index"))
    task.status = 0
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = db.session.query(Task).filter(Task.id == task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
