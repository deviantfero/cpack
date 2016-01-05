#!/usr/bin/python
from sys import argv
import os.path
from os import walk
from subprocess import call
import split
from gi import require_version
require_version( "Gtk", "3.0" )
from gi.repository import Gtk, GLib


dict = { "Dec": 11, "Nov": 10, "Oct": 9, "Sep": 8, "Aug": 7, "Jul": 6, "Jun": 5, "May": 4, "Apr": 3, "Mar": 2, "Feb": 1, "Jan":0 }

def get_active_info( directory ):
    active_info = open( directory, "r" )
    string = active_info.read()
    return string

def get_combo_text( directory ):
    active_info = open( directory, "r" )
    string = active_info.readline( 1 )
    return string

class filelistget():

    def __init__( self, directory ):
        self.directory = directory
        self.file_list = []
        for ( dirpath, dirnames, filenames ) in walk( self.directory ):
            self.file_list.extend( filenames )
        self.file_list = [ word for word in self.file_list if not "." in word ]

class dates_init():
    
    def __init__( self, date_filepath ):
        date_file = open( date_filepath, "r" )
        self.full_dates = [ line for line in date_file ]
        date_file.close() #--we don't need the file open anymore--#
        self.full_dates = [ line.split( " ", len( line ) ) for line in self.full_dates ]
        self.months = [ word[0] for word in self.full_dates ]
        self.days   = [ word[1] for word in self.full_dates ]
        daystring = "".join( self.days )
        self.days = daystring.split( ",", len( daystring ) )
        self.days.pop()
        self.days   = [ int( word ) for word in self.days ]
        self.years  = [ int( word[2] ) for word in self.full_dates ]
        self.months = [ int( dict[word] )for word in self.months ]
        self.full_dates = []
        for x in range( 0, len( self.days ) ):
            self.full_dates.append( [ self.years[x], self.months[x], self.days[x] ] )

class mainWindow( Gtk.Window ):

    def __init__( self ):

        self.tracking_directory = GLib.get_home_dir() + "/.tracking/"
        self.files = filelistget( self.tracking_directory )
        print( self.files.file_list )
        self.tracking_active = ""
        self.info_list = []

        Gtk.Window.__init__( self, title="cpack v1.0" )
        self.set_border_width( 10 )
        self.set_default_size( 600, 100 )

        self.parent_grid = Gtk.Grid()
        self.parent_grid.set_row_spacing( 10 )
        self.parent_grid.set_column_spacing( 20 )
        self.child_grid = Gtk.Grid()
        self.child_grid.set_row_spacing( 5 )
        self.child_grid.set_column_spacing( 10 )
        self.child_grid.set_column_homogeneous( True )
        self.layout_grid = Gtk.Grid()
        self.refresh_button = Gtk.Button( "Refresh" )
        self.refresh_button.connect( "clicked", self.refresh_action )
        self.add_button = Gtk.Button( "Add" )
        self.add_button.connect( "clicked", self.add_action )
        self.rm_button = Gtk.Button( "Remove" )
        self.rm_button.connect( "clicked", self.rm_action )
        self.add( self.parent_grid )

        self.info_label = Gtk.Label("No tracking number selected")
        self.info_label.set_selectable( True )
        self.info_label.set_line_wrap( False )
        self.info_label.set_justify( Gtk.Justification.FILL )
        self.layout = Gtk.Layout()
        self.layout.set_size( 200, 900 )
        self.layout.set_vexpand( True )
        self.layout.set_hexpand( True )
        self.layout.put( self.info_label, 0, 0 )
        self.vadjustment = self.layout.get_vadjustment()
        self.hadjustment = self.layout.get_hadjustment()
        self.vscrollbar = Gtk.Scrollbar( orientation=Gtk.Orientation.VERTICAL, adjustment=self.vadjustment )
        self.hscrollbar = Gtk.Scrollbar( orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.hadjustment )
        self.layout_grid.attach( self.layout, 0, 0, 1, 1 )
        self.layout_grid.attach( self.vscrollbar, 1, 0, 1, 1 )

        self.tracking_input = Gtk.Entry()
        self.tracking_input.set_text( "Copy tracking number here" )

        self.calendar = Gtk.Calendar()
        self.calendar.connect( "month-changed", self.month_refresh_marks )
        
        self.combo_list = Gtk.ListStore( str )
        for word in self.files.file_list:
            letter = get_combo_text( self.tracking_directory + word )
            print( letter )
            self.combo_list.append( [ letter ] )
        self.combo = Gtk.ComboBox.new_with_model( self.combo_list )
        self.combo.set_entry_text_column(0)
        self.text_render = Gtk.CellRendererText()
        self.combo.pack_start( self.text_render, True )
        self.combo.add_attribute( self.text_render, "text", 0 )
        self.combo.connect( "changed", self.combo_change )
        #--attaching--#
        self.parent_grid.attach( self.child_grid, 0, 1, 1, 1 )
        self.parent_grid.attach( self.calendar,   0, 0, 1, 1 )
        self.child_grid.attach( self.tracking_input, 0, 0, 2, 1 )
        self.child_grid.attach( self.add_button,     0, 1, 2, 1 )
        self.child_grid.attach( self.combo,          0, 2, 2, 1 )
        self.child_grid.attach( self.refresh_button, 0, 3, 1, 1 )
        self.child_grid.attach( self.rm_button, 1, 3, 1, 1 )
        self.parent_grid.attach( self.layout_grid, 1, 0, 1, 2 )

        self.active_dates_status = False

    def update_combo( self ):
        self.files = filelistget( self.tracking_directory )
        self.combo_list = Gtk.ListStore( str )
        for word in self.files.file_list:
            letter = get_combo_text( self.tracking_directory + word )
            print( letter )
            self.combo_list.append( [ letter ] )
        self.combo.set_model( self.combo_list )

    def refresh_action( self, refresh_button ):
        print( "refresh" )
        self.calendar.clear_marks()
        self.tracking_active = self.files.file_list[self.combo.get_active()]
        split.splitfile( self.tracking_active )
        info = get_active_info( self.tracking_directory + self.tracking_active )
        self.active_dates = dates_init( self.tracking_directory + self.tracking_active + ".dte" )
        self.mark_calendar( self.active_dates )
        self.info_label.set_text( self.tracking_active + "\n" + info )

    def add_action( self, add_button ):
        print( "add" )
        split.splitfile( self.tracking_input.get_text() )
        self.update_combo()
    
    def rm_action( self, rm_button ):
        print( "rm" )
        call( ["rm", self.tracking_directory + self.tracking_active] )
        call( ["rm", self.tracking_directory + self.tracking_active + ".dte"] )
        self.update_combo()

    def mark_calendar( self, active_dates ):
        current_date = self.calendar.get_date()
        print( current_date )
        for word in active_dates.full_dates:
            if( word[0] == current_date[0] and word[1] == current_date[1] ):
                self.calendar.mark_day( word[2] )
            else:
                self.calendar.unmark_day( word[2] )

    def month_refresh_marks( self, calendar ):
        self.calendar.clear_marks()
        if( self.active_dates_status ):
            self.mark_calendar( self.active_dates )

    def combo_change( self, combo ):
        self.calendar.clear_marks()
        self.info_list = []
        self.tracking_active = self.files.file_list[combo.get_active()]
        print( self.tracking_active )
        info = get_active_info( self.tracking_directory + self.tracking_active )
        self.info_list = info.split( "\n", len(info) )
        print( self.info_list )
        #later use with calendar
        self.info_label.set_text( self.tracking_active + "\n" + info )
        self.active_dates = dates_init( self.tracking_directory + self.tracking_active + ".dte" )
        self.active_dates_status = True
        self.mark_calendar( self.active_dates )


if __name__ == "__main__":
    main_win = mainWindow()
    main_win.connect( "delete-event", Gtk.main_quit )
    main_win.show_all()
    Gtk.main()
