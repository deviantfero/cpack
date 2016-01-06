#!/usr/bin/python
from sys import argv
import os.path
from os import walk
from subprocess import call

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
    print( "TESTING CONNECTION::" )
    internet = call( ["ping", "-c", "1", "google.com"] )
    if( internet == 2 ):
        print( "NO INTERNET::" )
        return
    print( "DOWNLOADING::" )
    call( [ "wget", "-O", tracking_dir + "/" + filename, "http://track.aftership.com/" + filename ] )
    print( "DONE::" )
    html = open( tracking_dir + filename, "r" )
    result_file = open( tracking_dir + "temp.cpk", "w+" )
    html_text = "\n".join( html.readlines() )
    #this joins the lines stored as a list with a '\n'
    #in between, so it can be split by string method split()
    result_list = html_text.split( "<div" )
    print( "PASS0::" ) #debug line
    print( "PASS1::" )
    result_list = [ word for word in result_list if "timeline" in word or "hint" in word ]
    for word in result_list:
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
        result_file.writelines( chr( number ) + "\n" )
    temp_cpk = open( tracking_dir + "temp.cpk", "r" )
    scan_captcha = temp_cpk.read()

    if "captcha" in scan_captcha and len(info) < 50:
        if( "There's a Cap" in full_bak ):
            print( "USING FULL BACK - STILL CAPTCHA::" )
            result_file.write( full_bak )
        else:
            print( "CAPTCHA ALERT::" )
            result_file.write( "\nThere's a Captcha! - no info fetched" + full_bak )
    else:
        result_file.write( info )
    call( ["rm", tracking_dir + "temp.cpk"] )

if __name__ == "__main__":
    splitfile( argv[1] )
