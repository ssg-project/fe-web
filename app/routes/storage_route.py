from flask import  Blueprint

storage_bp = Blueprint('storage', __name__, url_prefix='/storage')

@storage_bp.route('/list', methods=['GET', 'POST'])
def get_list_files():
    return "start"