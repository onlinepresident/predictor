from flask import render_template,url_for,redirect, flash,request
from app.forms import LoginForm, TeamForm,PredictionForm,UserForm
from app import app, db
from app.models import User, Team, Prediction,PredictionView
from flask_login import current_user, login_user,logout_user,login_required
from app.tables import PredictionTable,UserTable,TeamTable
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select, update, delete

#model related libraries
import pickle
import numpy as np
model = pickle.load(open('ml_model.pkl', 'rb'))


@app.route('/')
@app.route('/index')
@login_required
def index():
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=current_user.username).first()
    #is_admin = User.query.filter_by(username=current_user.username).first()
    #accounts = db.session.execute('select count(id) as c from user').scalar()
   # documents = DocumentSource.query.join(Document, DocumentSource.id==Document.source_id).add_columns(Document.id, Document.subject , Document.insert_date, Document.priority, DocumentSource.source).filter_by(user_id = user.id).order_by(Document.insert_date.desc()).paginate(page,app.config['DOCUMENTS_PER_PAGE'], False)

    total_prediction_count=Prediction.query.count()
    predictions = PredictionView.query.filter_by(user_id = user.id).order_by(PredictionView.prediction_date.desc()).paginate(page,app.config['DOCUMENTS_PER_PAGE'], False)
    next_url = url_for('index', page=predictions.next_num) if predictions.has_next else None
    prev_url = url_for('index', page=predictions.prev_num) if predictions.has_prev else None

    return render_template('./index.html', predictions=predictions.items, title='Home', next_url=next_url, prev_url=prev_url,total_prediction_count=total_prediction_count)

@app.route('/inbox')
@login_required
def inbox():
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=current_user.username).first()

    total_prediction_count=Prediction.query.count()
#    predictions = Prediction.query.filter_by(user_id = user.id).order_by(Prediction.insert_date.desc()).paginate(page,app.config['DOCUMENTS_PER_PAGE'], False)
    predictions = PredictionView.query.filter_by(user_id = user.id).order_by(PredictionView.prediction_date.desc()).paginate(page,app.config['DOCUMENTS_PER_PAGE'], False)
    next_url = url_for('index', page=predictions.next_num) if predictions.has_next else None
    prev_url = url_for('index', page=predictions.prev_num) if predictions.has_prev else None

    return render_template('./index.html', predictions=predictions.items, title='Home', next_url=next_url, prev_url=prev_url,total_prediction_count=total_prediction_count)


@app.route('/all_predictions', methods=['GET','POST'])
@login_required
def all_predictions():
    # qry = text( """
    #         select * from v_all_predictions;
    #
    #     """)
    # predictions =     db.session.execute(qry)
    predictions =     PredictionView.query.all()
    table = PredictionTable(predictions)
    return render_template('./all_predictions.html', predictions=predictions,table=table)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('The username or the password is wrong')
            return redirect(url_for('login'))
        login_user(user,form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('./login.html', form=form, title = 'Sign In')

@app.route('/predict', methods=['GET','POST'])
@login_required
def predict():
    # home_team_id      = request.values.get('away_team')
    # away_team_id      = request.values.get('away_team')
    # h_odd           = request.values.get('h_odd')
    # d_odd           = request.values.get('d_odd')
    #
    # array             = np.array([[home_team_id, away_team_id, h_odd, d_odd]])
    # model_prediction            = float(model.predict(array))

    user = User.query.filter_by(username=current_user.username).first()
    latest_prediction='None'
    form = PredictionForm()
    if form.validate_on_submit():
        home_team = request.form.get('home_team')
        away_team = request.form.get('away_team')
        h_odd           = request.values.get('h_odd')
        d_odd           = request.values.get('d_odd')

        array             = np.array([[home_team, away_team, h_odd, d_odd]])
        model_prediction            = float(model.predict(array))

        if model_prediction==2:
            winner = home_team
        elif model_prediction==1:
            winner=away_team
        else:
            winner = 'Draw Game'

        prediction = Prediction(
        user_id = user.id
        ,home_team = home_team
        ,away_team= away_team
        ,winner = winner
        )

        db.session.add(prediction)
        db.session.commit()
        flash('Prediction saved successfully')


        return redirect(url_for('predict'))
    latest_prediction = PredictionView.query.filter_by(user_id=user.id).order_by(PredictionView.prediction_date.desc()).first()
    return render_template('./predict.html', form =form, latest_prediction=latest_prediction)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    users = User.query.all()
    table = UserTable(users)
    form = UserForm()
    if form.validate_on_submit():
        user = User(
        username=form.username.data
        ,email=form.email.data
        ,is_admin=False
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('New user is created successfully')
        return redirect(url_for('add_user'))
    return render_template('./add_user.html', form =form,users=users,table=table)


@app.route('/add_team', methods=['GET','POST'])
def add_team():
    user = User.query.filter_by(username=current_user.username).first()
    teams = Team.query.all()
    table = TeamTable(teams)
    form = TeamForm()


    if form.validate_on_submit():
        team =Team(
        name=form.name.data
        )

        db.session.add(team)
        db.session.commit()
        flash('New Team is added successfull')
        return redirect(url_for('add_team'))
    return render_template('./add_team.html',form=form,table=table)

@app.route('/delete_team/<int:id>', methods=['GET', 'POST'])
def delete_team(id):
    # team = db.session.get(Team, id)
    # db.session.delete(team)
    # db.session.commit()
    team = delete(Team).where(Team.id==id)
    db.session.execute(team)
    db.session.commit()

    teams = Team.query.all()
    table = TeamTable(teams)
    form = TeamForm()

    return render_template('./add_team.html',form=form,table=table)



@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    # team = db.session.get(Team, id)
    # db.session.delete(team)
    # db.session.commit()
    user = delete(User).where(User.id==id)
    db.session.execute(user)
    db.session.commit()

    users = User.query.all()
    table = UserTable(user)
    form = UserForm()

    return render_template('./add_user.html', form =form,users=users,table=table)
