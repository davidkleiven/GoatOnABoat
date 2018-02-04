class Question(object):
    """
    Base class for all questions
    """
    def __init__(self):
        pass

    def get( self ):
        raise NotImplementedError( "This function has to be implemented in derived classes!" )

    def alternatives(self):
        raise NotImplementedError( "This function has to be implemented in derived classes!" )
