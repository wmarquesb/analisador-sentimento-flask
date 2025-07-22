from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func

from app import db, bcrypt
from app.models import User, Feedback
from app.ai_service import analyze_sentiment

auth = Blueprint('auth', __name__)

@auth.route("/")
def index():
    """Redireciona o usuário para o login ou para o dashboard."""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

@auth.route("/dashboard")
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    pagination = Feedback.query.filter_by(author=current_user).order_by(Feedback.submission_date.desc()).paginate(page=page, per_page=5)
    return render_template('dashboard.html', pagination=pagination)

@auth.route("/analyze", methods=['POST'])
@login_required
def analyze():
    feedback_text = request.form.get('feedback_text')
    if feedback_text:
        sentiment = analyze_sentiment(feedback_text)
        new_feedback = Feedback(text_content=feedback_text, author=current_user, sentiment_result=sentiment)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Seu feedback foi analisado com sucesso!', 'success')
    return redirect(url_for('auth.dashboard'))

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        user = User(username=request.form.get('username'), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi criada! Você já pode fazer login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            flash(f'Login bem-sucedido. Bem-vindo, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('auth.dashboard'))
        else:
            flash('Login sem sucesso. Por favor, verifique o usuário e a senha.', 'danger')
    return render_template('login.html')

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/reanalyze/<int:feedback_id>")
@login_required
def reanalyze_feedback(feedback_id):
    feedback_to_analyze = Feedback.query.get_or_404(feedback_id)
    if feedback_to_analyze.author != current_user:
        flash('Operação não permitida.', 'danger')
        return redirect(url_for('auth.dashboard'))
    
    sentiment = analyze_sentiment(feedback_to_analyze.text_content)
    feedback_to_analyze.sentiment_result = sentiment
    db.session.commit()
    
    flash('Feedback re-analisado com sucesso!', 'success')
    return redirect(url_for('auth.dashboard'))

@auth.route("/delete/<int:feedback_id>")
@login_required
def delete_feedback(feedback_id):
    feedback_to_delete = Feedback.query.get_or_404(feedback_id)
    if feedback_to_delete.author != current_user:
        flash('Operação não permitida.', 'danger')
        return redirect(url_for('auth.dashboard'))

    db.session.delete(feedback_to_delete)
    db.session.commit()
    flash('Feedback apagado com sucesso.', 'success')
    return redirect(url_for('auth.dashboard'))

@auth.route('/api/dashboard-stats')
@login_required
def dashboard_stats():
    total_feedbacks = db.session.query(func.count(Feedback.id)).filter_by(author=current_user).scalar()
    sentiment_distribution = db.session.query(
        Feedback.sentiment_result, func.count(Feedback.sentiment_result)
    ).filter_by(author=current_user).group_by(Feedback.sentiment_result).all()
    
    stats = {
        'total': total_feedbacks,
        'sentiments': {'Positivo': 0, 'Negativo': 0, 'Neutro': 0}
    }
    for sentiment, count in sentiment_distribution:
        if sentiment in stats['sentiments']:
            stats['sentiments'][sentiment] = count
            
    return jsonify(stats)