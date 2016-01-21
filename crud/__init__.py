from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )
from .security import groupfinder
from pyramid.security import (
    Allow,
    Authenticated,
    Everyone,Deny,)


class RootFactory(object):
    __name__ = ""
    __acl__ = [(Allow, Authenticated, 'registered')]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    fearfactory = UnencryptedCookieSessionFactoryConfig('0', timeout=None)
    authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, session_factory=fearfactory, root_factory=RootFactory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('login', '/login')
    config.add_route('home', '/')
    config.add_route('deleteuser', '/delete/{uid}')
    config.add_route('user', '/user/{uid}')
    config.add_route('newuser', '/newuser')
    config.add_route('logout', '/logout')
    config.add_route('signup', '/signup')
    config.scan()
    return config.make_wsgi_app()
