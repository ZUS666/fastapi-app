from sqladmin import ModelView

from repositories.sql_db.models import Profile, User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.user_id,
        User.email,
        User.is_active,
        User.is_stuff,
        User.is_super_user,
        User.profile,
    ]


class ProfileAdmin(ModelView, model=Profile):
    columnn_list = [
        Profile.user_id,
        Profile.first_name,
        Profile.last_name,
    ]