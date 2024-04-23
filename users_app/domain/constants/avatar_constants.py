import enum


class AvatarAllowTypes(enum.StrEnum):
    jpeg = 'image/jpeg'
    png = 'image/png'


AVATAR_BUCKET = 'avatars/'
AVATAR_MAX_SIZE = 5 * 1024 * 1024
