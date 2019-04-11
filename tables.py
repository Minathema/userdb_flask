from flask_table import Table, Col, LinkCol

class Results(Table):
    id = Col('ID', show=False)
    user_name = Col('NAME')
    mobile_number = Col('MOBILE NUMBER')
    email = Col('EMAIL')
    home_address = Col('HOME ADDRESS')
    edit = LinkCol('Edit', 'edit_view', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_user', url_kwargs=dict(id='id'))
