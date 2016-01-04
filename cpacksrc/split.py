#!/usr/bin/python
from sys import argv
import os.path
from subprocess import call

def splitfile( filename ):
    filename = filename.upper()
    tracking_dir = os.path.expanduser( "~" ) + "/.tracking/"
    if( not os.path.isdir( tracking_dir ) ):
        call( [ "mkdir", tracking_dir ] )
    if( os.path.isfile( filename ) ):
        call( ["rm", filename] )
    call( [ "wget", "-O", tracking_dir + "/" + filename, "http://track.aftership.com/" + filename ] )
    html = open( tracking_dir + filename, "r" )
    result_file = open( tracking_dir + "temp.cpk", "w+" )
    html_text = "\n".join( html.readlines() )
    #this joins the lines stored as a list with a '\n'
    #in between, so it can be split by string method split()
    result_list = html_text.split( "<div" )
    print( result_list ) #debug line
    result_list = [ word for word in result_list if "timeline" in word or "hint" in word ]
    for word in result_list:
        result_file.write( word )
    result_file.close()
    html.close()
    if not os.path.isfile( tracking_dir + "/.parser" ):
        if os.path.isfile( "./parser.c" ):
            print( "compiling from test dir" )
            call( [ "cc", "-o", tracking_dir + ".parser", "./parser.c" ] )
        else:
            print( "compiling from /usr/local/bin" )
            call( [ "cc", "-o", tracking_dir + ".parser", "/usr/local/bin/parser.c" ] )
    call( [ tracking_dir + ".parser", filename ] )
    call( ["rm", tracking_dir + "temp.cpk"] )

if __name__ == "__main__":
    splitfile( argv[1] )
