import datetime
import bcrypt as bcrypt
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import view_config, forbidden_view_config
from sqlalchemy.exc import InterfaceError
from .models import (
    DBSession,
    Users,
    )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.resource_url(request.context),
                     headers=headers)


@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    login_url = request.resource_url(request.context, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from (loop)
    came_from = request.params.get('came_from', referrer)
    message = ''
    loginstring = ''
    password = ''
    if 'form.submitted' in request.params:
        loginstring = str(request.params['email'])
        password = str(request.params['password']).encode()
        try:
            user = DBSession.query(Users).filter(Users.email == loginstring).first()
            pass_encoded = str(user.password).encode()
            if user is not None:
                print bcrypt.hashpw(password, pass_encoded)
                if bcrypt.hashpw(password, pass_encoded) == pass_encoded:
                    request.session['email'] = str(user.email)
                    headers = remember(request, loginstring)
                    request.session['display_name'] = str(user.first_name + " " + user.last_name)
                    user.last_login = datetime.datetime.now()
                    return HTTPFound(location='/',
                                     headers=headers)
                else:
                    message = 'Invalid Username or Password.'
            else:
                message = 'Invalid Username or Password.'
        except InterfaceError:
            message = "Error connecting to database."
    return {
        'message': message,
        'url': request.application_url + '/',
        'came_from': came_from,
        'email': loginstring,
        'password': password,
    }


@view_config(route_name='signup', renderer='templates/signup.pt')
def signup(request):
    error = None
    if 'form.submit' in request.POST:
        email = request.POST['email']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        dob = datetime.datetime.strptime(request.POST['dob'], '%Y-%m-%d')
        zip_code = request.POST['zipcode']
        password = str(request.POST['password'])
        if len(email) > 1:
            checkemail = DBSession.query(Users).filter(Users.email == email).first()
            if checkemail is None:
                password = bcrypt.hashpw(password, bcrypt.gensalt(prefix=b"2a"))
                newuser = Users(email=email, password=password, first_name=first_name,
                                last_name=last_name, dob=dob, zip_code=zip_code,
                                created_ts=datetime.datetime.now())
                DBSession.add(newuser)
                DBSession.flush()
                return HTTPFound(location='/')
            if checkemail is not None:
                error = 'User already exists'
        else:
            error = 'Please enter a valid Email address'
    return {'pagetitle': "Sign Up",
            'message': error}
