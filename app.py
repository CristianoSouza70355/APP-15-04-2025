from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///frequencia.db'
db = SQLAlchemy(app)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)

class Frequencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    alunos = Aluno.query.all()
    return render_template('index.html', alunos=alunos)

@app.route('/registrar_frequencia', methods=['POST'])
def registrar_frequencia():
    aluno_id = request.form.get('aluno_id')
    data = datetime.strptime(request.form.get('data'), '%Y-%m-%d').date()
    presente = request.form.get('presente') == 'on'

    frequencia = Frequencia(aluno_id=aluno_id, data=data, presente=presente)
    db.session.add(frequencia)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)