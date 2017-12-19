# -*- coding: utf-8 -*-
"""
Example of use:

class SessionTransaction(object):
 
    def __init__(self, session, transaction_manager):
        self.session = session
        self.transaction_manager = transaction_manager

    def __enter__(self):
        session_transactor = SessionTransaction(self.session)
        data_manager = SessionDataManager(session_transactor)
        self.transaction_manager.join(data_manager)
        return session

    def __exit__(self, type, value, traceback):
        pass

"""

try:
    from transaction.interfaces import IDataManager
    from zope.interface import implementer
except ImportError:
    pass
else:

    class ISessionTransaction(Interface):
        """A transaction manager for a session.
        """
        session = Attribute('The session object.')
        
        def abort(self):
            pass

        def commit(self):
            pass

        def finish(self):
            pass


    @implementer(IDataManager)
    class SessionDataManager(object):
        """Generic session data manager for transactions.
        """
        def __init__(self, transactor):
            assert ISessionTransaction.providedBy(transactor)
            self.transactor = transactor

        def abort(self, transaction):
            self.transactor.abort()

        def tpc_begin(self, transaction):
            pass

        def commit(self, transaction):
            self.transactor.commit()

        def tpc_vote(self, transaction):
            pass

        def tpc_finish(self, transaction):
            self.transactor.finish()

        def tpc_abort(self, transaction):
            pass

        def sortKey(self):
            return "~cromlech.session"
