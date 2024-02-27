from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Float, String, Integer


app = Flask(__name__)
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///book-records.db"

database = SQLAlchemy(model_class=Base)
database.init_app(app=app)


class Records(database.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[int] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[str] = mapped_column(Float, nullable=False)


@app.route('/')
def home():
    result = database.session.execute(database.select(Records))
    all_books = result.scalars()

    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["name"]
        author = request.form["author"]
        rating = request.form["rating"]
        with app.app_context():
            database.create_all()

        with app.app_context():
            new_record = Records(title=title, author=author, rating=rating)
            database.session.add(new_record)
            database.session.commit()
        return redirect(url_for("home"))
    return render_template('add.html')


@app.route("/edit/<int:idn>", methods=["GET", "POST"])
def edit(idn):
    # TODO find the edited book and pass it to edit.html
    if request.method == "POST":
        book_id = request.form["id"]
        print(f"The book id is : {book_id}")
        print(f"The book id is : {idn}")
        # book = database.session.execute(database.select(Records).where(Records.id == book_id)).scalar() # TODO another
        #  way of fetching data
        book_2 = database.get_or_404(Records, idn)
        book_2.rating = request.form['rating'] # Todo Fetch the Rating input by the  user
        database.session.commit()
        return redirect(url_for("home"))

    current_book = database.session.execute(database.select(Records).where(Records.id == idn)).scalar()
    return render_template("edit.html", book=current_book, book_id=idn)


@app.route("/delete/<int:idn>")
def delete(idn):
    current_book = database.get_or_404(Records,idn)
    database.session.delete(current_book)
    database.session.commit()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
