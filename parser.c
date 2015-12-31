//this program will process the exit code of split.py
//and will fix the file to be more readable
#include <stdio.h>
#include <stdlib.h>
#define MAX 80

typedef struct {
	char* month;
	int day;
	int year;
	char* time;
	char* info;
	char* place;
}status;

status init_status();
void get_time( status* new, FILE* read_file );

int main( int argc, char* argv[] ) {
	int file_pos;
	FILE* read_file = fopen( "./result.cpk", "r+" );
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
	status new = init_status();
	get_time( &new, read_file );
}

status init_status() {
	status new;
	new.month = malloc( MAX );
	new.day   = 0;
	new.year  = 0;
	new.time  = malloc( MAX );
	new.info  = malloc( MAX );
	new.place = malloc( MAX );
	return new;
}

void get_time( status* new, FILE* read_file ) {
	int i = 0;
	while( !feof( read_file ) ){
		if( fscanf( read_file, "%s %d, %d", new->month, &(new->day), &(new->year) ) == 3 ) {
			//to be changed
			printf( "%s %d, %d - event %d\n", new->month, new->day, new->year, i );
			i++;
		}
	}
}
