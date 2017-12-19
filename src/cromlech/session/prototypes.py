# -*- coding: utf-8 -*-

class SessionHandler(object):
    """ HTTP session handler skeleton.
    """
    def __iter__(self):
        """Iterates the session ids if that makes sense in the context
        of the session management.
        """
        return iter(())

    def new(self):
        return {}

    def get(self, sid):
        raise NotImplementedError

    def set(self, sid, session):
        raise NotImplementedError

    def clear(self, sid):
        raise NotImplementedError

    def touch(self, sid):
        """This method is similar to the `touch` unix command.
        It will update the timestamps, if that makes sense in the
        context of the session. Example of uses : file, cookie, jwt...
        """
        pass

    def flush_expired_sessions(self):
        raise NotImplementedError


class Session(object):
    """ HTTP session dict prototype.
    This is an abstraction on top of a simple dict.
    It has flags to track modifications and access.
    Persistence should be handled and called exclusively
    in and through this abstraction.
    """
    def __init__(self, new, sid, handler):
        self.sid = sid
        self.handler = handler
        self.new = new  # boolean : this is a new session.
        self._modified = new or False
        self._session = None  # Lazy loading

    def __getitem__(self, key):
        return self.session[key]

    def __setitem__(self, key, value):
        self.session[key] = value
        self._modified = True

    def __delitem__(self, key):
        self.session.__delitem__(key)
        self._modified = True

    def __repr__(self):
        return self.session.__repr__()

    def __iter__(self):
        return iter(self.session)

    def __contains__(self, key):
        return key in self.session

    def has_key(self, key):
        return key in self.session

    def get(self, key, default=None):
        return self.session.get(key, default)

    @property
    def session(self):
        if self._session is None:
            if self.new:
                self._session = self.handler.new()
            else:
                self._session = self.handler.get(self.sid)
        return self._session

    @property
    def accessed(self):
        return self._session is not None

    @property
    def modified(self):
        return self._modified

    def save(self):
        """Mark as dirty to allow persistence.
        This is dramatically important to use that method to mark
        the session to be written. If this method is not called,
        only new sessions or forced persistence will be taken into
        consideration.
        """
        self._modified = True

    def persist(self, force=False):
        if force or (not force and self._modified):
            self.handler.set(self.sid, self.session)
            self._modified = False
        elif self.accessed:
            # We are alive, please keep us that way.
            self.handler.touch(self.sid)
