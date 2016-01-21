from .models import DBSession, Users
GROUPS = {'registered': ['group:registered']}


def groupfinder(email, request):
    user = DBSession.query(Users).filter(Users.email == email).first()
    if user is not None:
        if email == user.email:
            return GROUPS.get(email, [])
