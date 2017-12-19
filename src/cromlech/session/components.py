# -*- coding: utf-8 -*-

from biscuits import parse, Cookie
from datetime import datetime, timedelta
from functools import wraps
from itsdangerous import TimestampSigner
from uuid import uuid4
from .prototypes import SessionDict


class SignedCookieManager(object):

    session_dict = SessionDict
    
    def __init__(self, secret, handler, cookie='sid'):
        self.handler = handler
        self.delta = handler.delta  # lifespan delta in seconds.
        self.cookie_name = cookie
        self.signer = TimestampSigner(secret)

    def generate_id(self):
        return str(uuid4())

    def refresh_id(self, sid):
        return str(self.signer.sign(sid), 'utf-8')

    def verify_id(self, sid):
        # maybe we want an error handling here.
        return self.signer.unsign(signed_sid, max_age=self.delta)
    
    def get_id(self, cookie):
        if cookie is not None:
            morsels = parse(cookie)
            signed_sid = morsels.get(self.cookie_name)
            if signed_sid is not None:
                sid = self.verify_id(signed_sid)
                return False, str(sid, 'utf-8')
        return True, self.generate_session_id()

    def cookie(self, sid, expire, path="/", domain="localhost"):
        """We enforce the expiration.
        """
        # Refresh the signature on the sid.
        ssid = self.refresh_id(sid)

        # Create the cookie containing the ssid.
        cookie = Cookie(
            name=self.cookie_name, value=ssid, path=path,
            domain=domain, expires=expire)
        return str(cookie)

    def session(self, cookie):
        new, sid = self.get_id(cookie)
        return self.session_dict(sid, new, self.handler)


class WSGISessionManager(object):

    def __init__(self, manager, environ_key='session'):
        self.environ_key = environ_key
        self.manager = manager

    def __call__(self, app):

        @wraps(app)
        def session_wrapper(environ, start_response):

            def session_start_response(status, headers, exc_info=None):

                # Write down the session
                # This relies on the good use of the `save` method.
                session_dict = environ[self.environ_key]
                session_dict.persist()

                # Prepare the cookie and push it in the headers
                path = environ['SCRIPT_NAME'] or '/'
                domain = environ['HTTP_HOST'].split(':', 1)[0]
                expire = datetime.now() + timedelta(seconds=self.delta)
                cookie = self.manager.cookie(
                    session_dict.sid, expire, path, domain)
                headers.append(('Set-Cookie', cookie))

                # Return normally
                return start_response(status, headers, exc_info)

            session_dict = self.manager.session(environ.get('HTTP_COOKIE'))
            environ[self.environ_key] = session_dict
            return app(environ, session_start_response)

        return session_wrapper
