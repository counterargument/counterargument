from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
db = SQLAlchemy(app)

class Guest(db.Model):
 id = db.Column(db.Integer, primary_key=True)
 name = db.Column(db.String(30), nullable=False)
 phone = db.Column(db.String(15), nullable=False)
 people = db.Column(db.Integer, nullable=False)
 room = db.Column(db.Integer,  nullable=False, unique=True)
 days = db.Column(db.Integer, nullable=False)
 date = db.Column(db.DateTime, default=datetime.utcnow)

 def __repr__(self):
  return '<Guest %r>' % self.id

@app.route('/')
def index():
 return render_template('registration.html')

@app.route('/', methods=['POST'])
def register():
 name = request.form['name']
 phone = request.form['phone']
 people = int(request.form['people'])
 room = int(request.form['room'])
 days = int(request.form['days'])

 guest = Guest(name=name, phone='+7' + phone, people=people, room=room, days=days)

 db.session.add(guest)
 db.session.commit()
 return render_template('registration.html')

@app.route('/database')
def database():
 guests = Guest.query.order_by(Guest.date).all()
 return render_template('database.html' , guests=guests)

@app.route('/database/<int:id>')
def database_data(id):
 guest1 = Guest.query.get(id)
 return render_template('database_detail.html' , guest1=guest1)

@app.route('/database/<int:id>/delete')
def database_delete(id):
 guest_del = Guest.query.get_or_404(id)
 try:
  db.session.delete(guest_del)
  db.session.commit()
  return redirect(url_for('database'))
 except:
  return "Unknown Error"

@app.route('/database/<int:id>/edit', methods=['POST', 'GET'])
def database_edit(id):
 guest = Guest.query.get(id)
 if request.method == 'POST':
  guest.name = request.form['name']
  guest.phone = request.form['phone']
  guest.people = int(request.form['people'])
  guest.room = int(request.form['room'])
  guest.days = int(request.form['days'])

  try:
   db.session.commit()
   return redirect('/database')
  except:
   return "Unknown Error"
 else:

  return render_template('database_edit.html' , guest=guest)

if __name__ == '__main__':
 app.run(debug=True)

