from flask_table import Col, ButtonCol, DateCol, LinkCol, Table,DatetimeCol

class PredictionTable(Table):
    classes = ['table','table-striped','table-bordered','table-hover','table-sm ']
    id = Col('ID')
    home_team = Col('Home Team')
    away_team = Col('Away Team')
    winner = Col('Winner')
    # edit = LinkCol('Edit', 'edit_prediction', url_kwargs=dict(id='id'))
    # delete = LinkCol('Delete', 'delete_prediction', url_kwargs=dict(id='id'))

class UserTable(Table):
    classes = ['table','table-striped','table-bordered','table-hover','table-sm ']
    id = Col('ID')
    username = Col('Username')
    email = Col('Email')
    is_admin = Col('Is Admin')
    delete= LinkCol('Delete', 'delete_user', url_kwargs=dict(id='id'))
    # delete = LinkCol('Delete', 'delete_user', url_kwargs=

class TeamTable(Table):
    classes = ['table','table-striped','table-bordered','table-hover','table-sm '] # CSS Classes
    id = Col('ID')
    name = Col('Name')
    delete = LinkCol('Delete', 'delete_team', url_kwargs=dict(id='id'))
