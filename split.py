def splitfile( filename ):
    html = open( filename, "r" )
    result_file = open( "result.cpk", "w+" )
    html_text = html.readlines()
    result_list = html_text[2].split( "<div" )
    print( result_list )
    result_list = [ word for word in result_list if "timeline" in word or "hint" in word ]
    for word in result_list:
        result_file.write( word )
    result_file.close()
    html.close()

if __name__ == "__main__":
    splitfile( "Tracking.htm" )
