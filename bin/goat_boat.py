#!/usr/env/bin python

import sys
from gob.gui.app import App

def main( argv ):
    if ( len(argv) == 0 ):
        print ("No players given!")
    player_names = argv
    print( "The following players are going to transport goats:" )
    for name in player_names:
        print( name )
    print ( "All players starts with a goat!" )
    app = App( players=player_names )
    app.on_execute()

if __name__ == "__main__":
    main( sys.argv[1:] )
