import split
import os.path
from os import walk
from subprocess import call

def main_update():
    tracking_path = os.path.expanduser( "~" ) + "/.tracking/"
    files_to_update = split.get_number_files( tracking_path )
    for word in files_to_update:
        file_old = open( tracking_path + word, "r" )
        content_old = file_old.read()
        file_old.close()
        split.splitfile( word )
        file_new = open( tracking_path + word, "r" )
        content_new = file_new.read()
        if( content_old != content_new ):
            content_new = content_new.split( "\n\n", len( content_new ) )
            to_notify = content_new.pop( 0 )
            if( "SVSALA" in to_notify or "elivery" in to_notify ):
                call( [ "notify-send", word, to_notify ] )

        

if __name__ == "__main__":
    main_update()
