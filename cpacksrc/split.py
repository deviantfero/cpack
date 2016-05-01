#!/usr/bin/python
from sys import argv
import os.path
import urllib.request
from os import walk
from subprocess import call

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def get_number_files( directory ):
    file_list = []
    for ( dirpath, dirnames, filenames ) in walk( directory ):
        file_list.extend( filenames )
    file_list = [ word for word in file_list if not "." in word ]
    return file_list

def splitfile( filename ):
    refresh_status = False
    full_bak = ""
    filename = filename.upper()
    tracking_dir = os.path.expanduser( "~" ) + "/.tracking/"
    file_list = get_number_files( tracking_dir ) #list of existing files before adding a new one

    if( not os.path.isdir( tracking_dir ) ):
        call( [ "mkdir", tracking_dir ] )

    if( os.path.isfile( tracking_dir + filename ) ):
        letter_get = open( tracking_dir + filename )
        letter_bak = letter_get.readline( 1 )
        full_bak = letter_get.read()
        #call( ["rm", tracking_dir + filename] )
        refresh_status = True
    print( "DOWNLOADING::" )
    req = urllib.request.Request( "http://track.aftership.com/" + filename, None, hdr )
    download = urllib.request.urlopen( req )
    string_htm = download.read()
    string_htm = str( string_htm )
    first_write = open( tracking_dir + filename, "w" )
    first_write.write( string_htm )
    first_write.close()
    print( "DONE::" )
    html = open( tracking_dir + filename, "r" )
    result_file = open( tracking_dir + "temp.cpk", "w+" )
    html_text = "\n".join( html.readlines() )
    #this joins the lines stored as a list with a '\n'
    #in between, so it can be split by string method split()
    result_list = html_text.split( "<div" )
    print( "PASS0::" ) #debug line
    print( "PASS1::" )
    result_list = [ word for word in result_list if "checkpoint" in word or "hint" in word ]
    #addesd some filter tags to avoid having useless info in the textfile
    result_list = [ word for word in result_list if "sr-only" not in word and "media-" not in word ]
    result_list = [ word for word in result_list if "text-xs" not in word and "aftership.com" not in word ]
    #word sorrounding information was changed from "timeline" to "checkpoint__<something>"
    #therefore a change in the word to be found was to be made
    for word in result_list:
        if( not "\\n" in word ):
            #removes useless \n characters from strings by not allowing them
            print( word )
            result_file.write( word )
    result_file.close()
    html.close()

    if not os.path.isfile( tracking_dir + "/.parser" ):
        if os.path.isfile( "./parser.c" ):
            print( "compiling from test dir" )
            call( [ "cc", "--std=c99", "-o", tracking_dir + ".parser", "./parser.c" ] )
        else:
            print( "compiling from /usr/local/bin" )
            call( [ "cc", "--std=c99", "-o", tracking_dir + ".parser", "/usr/local/bin/cpacksrc/parser.c" ] )

    check = open( tracking_dir + "temp.cpk" )
    if( "checkpoint_" in check.read() ):
        #word sorrounding information was changed from "timeline" to "checkpoint__<something>"
        #therefore a change in the word to be found was to be made
        #weird bug here
        print( "PASS2::" )
        call( [ tracking_dir + ".parser", filename ] )
    print( "FINISHED::" )
    result_file = open( tracking_dir + filename, "r" )
    info = result_file.read()

    print( "INFO FETCH COMPLETE::" )
    print( info )
    result_file.close()
    info_list = info.split( "\n", len(info) )
    info = "" #clean up info is next

    print( "GETTING DATES::" )

    if( not os.path.isfile( tracking_dir + filename + ".dte" ) ):
        dates = open( tracking_dir + filename + ".dte", "w" )

    if( len( info_list ) > 4 ):
        dates = open( tracking_dir + filename + ".dte", "w" )
        for word in info_list:
            if( "," in word and len(word) < 18 ):
                info += "\n" + word + "\n"
                dates.write( word + "\n" )
            else:
                info += word + "\n"
        dates.close()

    print( file_list )
    number = 65
    letter = []
    for word in file_list:
        temp = open( tracking_dir + word, "r" )
        letter.append( temp.readline(1) )
        temp.close()
    letter.sort()

    if letter:
        print( "Found last letter::")
        number = ord( letter.pop() ) + 1
    else:
        print( "found no letter - assign first FILE::A" )

    result_file = open( tracking_dir + filename, "w" )
    if refresh_status:
        result_file.writelines( letter_bak )
    else:
        result_file.writelines( chr( number ) )
    temp_cpk = open( tracking_dir + "temp.cpk", "r" )
    scan_captcha = temp_cpk.read()

    if "captcha" in scan_captcha and len(info) < 50:
        print( "CAPTCHA ALERT::" )
        call( ["rm", tracking_dir + "temp.cpk"] )
        result_file.write( full_bak )
        return 2
    else:
        result_file.write( info )
    call( ["rm", tracking_dir + "temp.cpk"] )
    return 0

if __name__ == "__main__":
    splitfile( argv[1] )
