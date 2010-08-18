#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dieses Script zeigt einen Dialog an bevor Chromium mit dem ausgewählten Profil gestartet wird.

Benutzung:
    Wähle ein Profil und starte Chromium mit einem Klick auf ok.

Pfade:
    * Ort der Profile: /home/enaut/.config/ChromiumProfiles
    * Ausführbare Datei: /usr/bin/chromium-browser

License:
    is free software, you can redistribute or modify it under the terms of the GNU General Public License Version 2 or any later Version (see http://www.gnu.org/copyleft/gpl.html for details). 

    Please feel free to contact me (name: enaut.w host: googlemail.com).
"""

#imports
import gtk
import dircache
import os
import shutil

profileDirectory = "/home/enaut/.config/ChromiumProfiles"
chromiumExecutable = "/usr/bin/chromium-browser"

class ProfileSelector(gtk.Window):
    """A class that is the selection window and contains all the functions nessessary."""

    treeView=None

    def __init__(self):
        super(ProfileSelector, self).__init__()

        self.set_size_request(400,400)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_border_width(8)

        self.connect("key-press-event", self.keypress)
        self.connect("destroy", gtk.main_quit)
        self.set_title("Profile Selector")

        vbox = gtk.VBox(False, 8)
        self.hbox = gtk.HBox(False, 8)
        navigation = gtk.HBox(False,8)

        desc = gtk.Label("\nWähle ein Profil mit dem Chromium gestartet werden soll.\n")

        self.add_edit_buttons(self.hbox)
        self.add_list(self.hbox)
        self.add_navigation_buttons(navigation)

        vbox.pack_start(desc, False, False, 0)
        vbox.pack_start(self.hbox, True, True, 0)
        vbox.pack_end(navigation, False, False, 0)


        self.add(vbox)
        self.show_all()
        return

    def add_list(self, hbox):
        """Create and add the profilelist to the gtk treeView."""
        store = self.create_model()
        self.treeView = gtk.TreeView(store)
        self.treeView.connect("row-activated", self.on_activated)
        self.treeView.set_rules_hint(True)
        self.create_columns(self.treeView)

        hbox.pack_end(self.treeView, True, True, 0)
        return

    def add_edit_buttons(self, hbox):
        """Add the left buttonbar with the edit buttons to the hBox."""
        buttonbox= gtk.VBox(False, 2)

        button = gtk.Button(stock=gtk.STOCK_ADD)
        button.connect("clicked", self.on_add_clicked)
        buttonbox.pack_start(button, False, False, 0)

        button = gtk.Button(stock=gtk.STOCK_EDIT)
        button.connect("clicked", self.on_edit_clicked)
        buttonbox.pack_start(button, False, False, 0)
        
        button = gtk.Button(stock=gtk.STOCK_REMOVE)
        button.connect("clicked", self.on_remove_clicked)
        buttonbox.pack_start(button, False, False, 0)
        
        hbox.pack_start(buttonbox, False, False, 0)
        return

    def add_navigation_buttons(self, box):
        """Add the bottom navigation buttons to the vBox"""
        buttonbox= box

        button = gtk.Button(stock=gtk.STOCK_EXECUTE)
        button.connect("clicked", self.launchChromium)
        buttonbox.pack_end(button, False, False, 0)

        button = gtk.Button(stock=gtk.STOCK_CANCEL)
        button.connect("clicked", gtk.main_quit)
        buttonbox.pack_end(button, False, False, 0)

        return

    def create_model(self):
        """Populate the list of available Profiles."""
        store = gtk.ListStore(str)
        fileList = dircache.listdir(profileDirectory)
#        print fileList
        store.clear()
        for cur in fileList:
            store.append([cur])
        return store

    def create_columns(self, treeView):
        """Setup the listView."""
        renderText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Profil", renderText, text=0)
        column.set_sort_column_id(0)
        treeView.append_column(column)
        return

    def on_activated(self, widget, row, col):
        """Execute Chromium with the selected profile."""
#        print "selected"
        self.launchChromium(widget)
        return

    def on_add_clicked(self, widget):
        """Add a new profile after asking for its name."""
#        print "add clicked"

        newProfile = self.getProfileName(message="Geben sie den namen des neuen Profils an:")

        absolutePath = os.path.join(profileDirectory, newProfile)

        if (self.checkIfExists(absolutePath=absolutePath)):
            return

        os.mkdir(absolutePath)

        self.treeView.props.model = self.create_model()

        return

    def on_edit_clicked(self, widget):
        """Rename a profile."""
#        print "edit clicked"

        model, itr = self.treeView.get_selection().get_selected()
        itemsToMove =model.get(itr,0)
        item=itemsToMove[0]

        newProfile = self.getProfileName("Geben sie den neuen Namen des Profils %s ein:" % item)
        absolutePathOld = os.path.join(profileDirectory, item)
        absolutePathNew = os.path.join(profileDirectory, newProfile)

        if (self.checkIfExists(absolutePath = absolutePathNew)):
            return

        os.rename(absolutePathOld, absolutePathNew)

        self.treeView.props.model = self.create_model()
        return

    def on_remove_clicked(self, widget):
        """Delete a profile."""
        model, itr = self.treeView.get_selection().get_selected()

        itemsToDelete =model.get(itr,0)

#        print itemsToDelete
        
        for item in itemsToDelete:
            shutil.rmtree(os.path.join(profileDirectory, item))

        self.treeView.props.model = self.create_model()
        
        return

    def keypress(self, widget, event):
        """Exit on escape press"""
        if event.keyval == gtk.keysyms.Escape:
#            print "Escape pressed closing!"
            gtk.main_quit()
        return

    def launchChromium(self, widget):
        """Start Chromium with the selected profile.
        
        Do so by forking and closing th initial process."""
#        print "Launch Chromium!"

        model, itr = self.treeView.get_selection().get_selected()
        items =model.get(itr,0)
        item=items[0]

        absolutePath = os.path.join(profileDirectory, item)

        pid = os.fork()
        if pid == 0:
            os.execve(chromiumExecutable, [chromiumExecutable, "--user-data-dir=%s" % absolutePath,], os.environ)
        gtk.main_quit()
        return

    def dialogHelper(self, entry, dialog, response):
        dialog.response(response)

    def getProfileName(self, message):
        """Return the text entered in its dialogbox."""
        dialog = gtk.MessageDialog(
                None,
                gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_QUESTION,
                gtk.BUTTONS_OK,
                None)
        dialog.set_markup(message)
        entry = gtk.Entry()
        entry.connect("activate", self.dialogHelper, dialog, gtk.RESPONSE_OK)

        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label("Name:"),False,5,5)
        hbox.pack_end(entry)
        dialog.vbox.pack_end(hbox, True,True,0)
        dialog.show_all()
        dialog.run()
        text = entry.get_text()
        dialog.destroy()
        return text

    def checkIfExists(self, absolutePath):
        """Check if a Profile with that name already exists."""
        # User input is bad so we check if the Directory already exists.
        if(os.path.exists(absolutePath)):
            dialog = gtk.MessageDialog(
                parent=self,
                flags=gtk.DIALOG_DESTROY_WITH_PARENT|gtk.DIALOG_MODAL,
                type=gtk.MESSAGE_ERROR,
                buttons=gtk.BUTTONS_CANCEL,
                message_format="Das Profil existiert bereits")
            dialog.show_all()
            dialog.run()
            dialog.destroy()
            return True
        else:
            return False


print __name__
if(__name__=="__main__"):
    prof = ProfileSelector()
    gtk.main()
