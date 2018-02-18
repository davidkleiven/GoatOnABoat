
class DirtyTrick(object):
    def __init__( self, key=None, info=None, cost=0 ):
        if ( key is None ):
            raise ValueError( "No key specified!" )

        if ( info is None ):
            raise ValueError( "No descriptive string is given!" )

        self.key = key
        self.info = info
        self.cost = cost

    def update(self):
        """
        Updates info of the class if nessecary
        """
        pass

    def update_game_mode(self):
        raise NotImplementedError( "This function has to be implemented in child classes!" )

    def apply( self ):
        raise NotImplementedError( "This function has to be implemented in child classes!" )
