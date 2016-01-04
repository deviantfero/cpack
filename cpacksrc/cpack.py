#!/usr/bin/python
from sys import argv
import os.path
from os import walk
from subprocess import call
import split
from gi import require_version
require_version( "Gtk", "3.0" )
from gi.repository import Gtk, GLib

def get_active_info( directory ):
    active_info = open( directory, "r" )
    string = active_info.read()
    return string

class filelistget():

    def __init__( self, directory ):
        self.directory = directory
        self.file_list = []
        for ( dirpath, dirnames, filenames ) in walk( self.directory ):
            self.file_list.extend( filenames )
        self.file_list = [ word for word in self.file_list if not "." in word ]

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
        
        self.combo_list = Gtk.ListStore( str )
        counter = 65
        for word in self.files.file_list:
            self.combo_list.append( [chr(counter)] )
            counter += 1
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

    def update_combo( self ):
        self.files = filelistget( self.tracking_directory )
        self.combo_list = Gtk.ListStore( str )
        for word in self.files.file_list:
            self.combo_list.append( [word] )
        self.combo.set_model( self.combo_list )

    def refresh_action( self, refresh_button ):
        print( "refresh" )

    def add_action( self, add_button ):
        print( "add" )
        call( ["python","./split.py", self.tracking_input.get_text() ] )
        self.update_combo()
    
    def rm_action( self, rm_button ):
        print( "rm" )
        call( ["rm", self.tracking_directory + self.tracking_active] )
        self.update_combo()
    
    def combo_change( self, combo ):
        self.info_list = []
        self.tracking_active = self.files.file_list[combo.get_active()]
        print( self.tracking_active )
        info = get_active_info( self.tracking_directory + self.tracking_active )
        self.info_list = info.split( "\n", len(info) )
        info = "" #clean up info is next
        for word in self.info_list:
            if( "," in word ):
                info += "\n" + word + "\n"
            else:
                info += word + "\n"
        print( self.info_list )
        self.info_label.set_text( self.tracking_active + "\n" + info )


if __name__ == "__main__":
    main_win = mainWindow()
    main_win.connect( "delete-event", Gtk.main_quit )
    main_win.show_all()
    Gtk.main()
