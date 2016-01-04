//this program will process the exit code of split.py
//and will fix the file to be more readable
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#define MAX 300
#define MAX_EVENTS 20
#define MAX_DESCR 50

int count_lines( FILE* write_file );
void clean_character( char rm_char, FILE* read_file );
void remove_newlines( FILE* read_file );
void clean_file_write( FILE* read_file, FILE* write_file );
int detect_character( char* string, char detect );

int main( int argc, char* argv[] ) {
	char* tracking_dir = strcat( getenv( "HOME" ), "/.tracking" );
	chdir( tracking_dir );
	if( argc < 2 ) {
		printf( "No output filename specified\n" );
		exit(1);
	}
	int file_pos;
	FILE* read_file = fopen( "./temp.cpk", "r+" );
	FILE* write_file = fopen( argv[1], "w+" );
	while( !feof( read_file ) ) {
		if( fgetc( read_file ) == '<' ) {
			fputs( ">\n", read_file );
		}
	}
	rewind( read_file );
	while( !feof( read_file ) ) {
		if( fgetc( read_file ) == '>' ) {
			fseek( read_file, -2, SEEK_CUR );
			fputs( ">\n", read_file );
		}
	}
	rewind( read_file );
	clean_character( '>', read_file );
	rewind( read_file );
	remove_newlines( read_file );
	clean_file_write( read_file, write_file );
	if( count_lines( write_file ) <= 2 ) {
		fclose( write_file );
		write_file = fopen( argv[1], "w+" );
		fputs( "No information was found at the time\n", write_file );
	}
}

void clean_character( char rm_char, FILE* read_file ) {
	while( !feof( read_file ) ) {
		if( fgetc( read_file ) == rm_char ) {
			fseek( read_file, -1, SEEK_CUR );
			fputc( ' ', read_file );
		}
	}
}

void remove_newlines( FILE* read_file ) {
	char* string = malloc( MAX );
	while( !feof( read_file ) ) {
		fgets( string, MAX, read_file );
		if( string[0] == '\n' || string[1] == '\n' ) {
			fseek( read_file, -1, SEEK_CUR );
			fputc( ' ', read_file );
		}
	}
}

void clean_file_write( FILE* read_file, FILE* write_file ) {
	rewind( read_file );
	char* string = malloc( MAX );
	while( !feof( read_file ) ) {
		fgets( string, MAX, read_file );
		if( strlen( string ) < MAX_DESCR && string[0] != ' ' && !detect_character( string, '{' ) ){
			fputs( string, write_file );
			printf( "%s", string );
		}
	}
}

int count_lines( FILE* write_file ) {
	int i = 0;
	rewind( write_file );
	while( !feof( write_file ) ) {
		if( fgetc( write_file ) == '\n' )
			i++;
	}
	printf( "%d\n", i );
	return i;
}

int detect_character( char* string, char detect ) {
	for( int i = 0; i < strlen( string ); i++ ) {
		if( string[i] == detect )
			return 1;
	}
	return 0;
}
