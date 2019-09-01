from alayatodo import login_manager
from alayatodo.dao import user as dao


@login_manager.user_loader
def load_user(user_id):
    return dao.load_user(user_id)
