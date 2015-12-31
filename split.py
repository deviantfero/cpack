def splitfile( filename ):
    html = open( filename, "r" )
    result_file = open( "result.cpk", "w+" )
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

if __name__ == "__main__":
    splitfile( "Tracking.htm" )
