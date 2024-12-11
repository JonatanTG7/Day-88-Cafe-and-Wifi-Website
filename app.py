from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

##CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"

# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)

#Create Table
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False )
    map_url: Mapped[str] = mapped_column(db.String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(db.String(500), nullable=False)
    location: Mapped[str] = mapped_column(db.String(250), nullable=False)
    has_sockets: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    has_toilet: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    seats: Mapped[str | None] = mapped_column(db.String(250), nullable=True)
    coffee_price: Mapped[str | None] = mapped_column(db.String(250), nullable=True)

    #this will allow each cafe object to be identified by its name when printed.
    def __repr__(self):
        return f'<Cafe {self.name}>'
    
# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('show_all_cafes'))

@app.route('/cafes')
def show_all_cafes():
    all_cafes = db.session.query(Cafe).all()
    return render_template("index.html" , cafes=all_cafes)

@app.route('/cafe/<int:cafe_id>')
def cafe_details(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    return render_template('cafe_details.html', cafe=cafe)

@app.route('/add', methods=['GET','POST'])
def add_cafe():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        img_url = request.form['img_url']
        map_url = request.form['map_url']
        has_wifi = 'has_wifi' in request.form
        has_sockets = 'has_sockets' in request.form
        has_toilet = 'has_toilet' in request.form
        can_take_calls = 'can_take_calls' in request.form
        seats = request.form['seats']
        coffee_price = request.form['coffee_price']


        new_cafe = Cafe(
            name=name,
            location=location,
            img_url=img_url,
            map_url=map_url,
            has_wifi=has_wifi,
            has_sockets=has_sockets,
            has_toilet=has_toilet,
            can_take_calls=can_take_calls,
            seats=seats,
            coffee_price=coffee_price
        )

        db.session.add(new_cafe)  
        db.session.commit() 
        # jsonify(response={"success": "Successfully added the new cafe."})
        return redirect(url_for('show_all_cafes'))
        
    return render_template('add_cafe.html')

@app.route('/delete/<int:cafe_id>', methods=['GET','POST'])
def delete_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)  
    db.session.delete(cafe)  
    db.session.commit()  
    return redirect(url_for('show_all_cafes'))  

@app.route('/update/<int:cafe_id>', methods=['GET','POST'])
def update_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)  
    if request.method == 'POST':
        cafe.name = request.form['name']
        cafe.location = request.form['location']
        cafe.img_url = request.form['img_url']
        cafe.map_url = request.form['map_url']
        cafe.has_wifi = 'has_wifi' in request.form
        cafe.has_sockets = 'has_sockets' in request.form
        cafe.has_toilet = 'has_toilet' in request.form
        cafe.can_take_calls = 'can_take_calls' in request.form
        cafe.seats = request.form['seats']
        cafe.coffee_price = request.form['coffee_price']

        db.session.commit()  
        return redirect(url_for('show_all_cafes'))  

    return render_template('update_cafe.html', cafe=cafe)

if __name__ == '__main__':
    app.run(debug=True)