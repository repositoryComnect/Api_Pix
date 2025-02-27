from flask import Blueprint, request, render_template, redirect, flash, url_for, session
from flask_login import login_user, logout_user, login_required
from settings.extensions import db
from application.models.models import User



login_bp = Blueprint('login', __name__)
# Crie o objeto admin


## ------------------------------------------- Bloco Rotas Login -------------------------------------------------------------------------------------------- ##
@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('authenticate.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('authenticate.login'))

    return render_template('register.html')




@login_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Busca o usuário no banco de dados
        user = User.query.filter_by(username=username).first()

        # Verifica se o usuário existe e se a senha está correta
        if user and user.password == password:  # Comparação simples de senha
            login_user(user)  # Autentica o usuário

            # Armazena o nome de usuário na sessão
            session['username'] = user.username

            return redirect(url_for('cob_imediata_tp.home'))  # Redireciona para a página sem enviar pela URL

        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')  # Exibe mensagem de erro

    return render_template('login.html')  # Renderiza o template de login





@login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('username', None)  # Remover o 'username' da sessão, se existir
    logout_user()
    return render_template('login.html')


