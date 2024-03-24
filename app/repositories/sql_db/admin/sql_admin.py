import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from core.database import Database
from repositories.sql_db.admin.admin_views import ProfileAdmin, UserAdmin


def build_admin(app: FastAPI):
    admin = Admin(app, Database().engine)
    admin.add_view(UserAdmin)
    admin.add_view(ProfileAdmin)
    return admin

if __name__ == '__main__':
    uvicorn.run('sql_admin:admin', host='0.0.0.0', port=8000, log_level='debug', reload=True)
