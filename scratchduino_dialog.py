# -*- coding: utf-8 -*-
__author__ = 'awangenh'

"""
@author: awangenh
Adaptations for usage with Scratchduino: Aldo von Wangenheim
Copyright (c) 2013-15 Iniciativa Computação na Escola

Adapted from http://effbot.org/tkinterbook

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from Tkinter import *
import os

class Dialog(Toplevel):

    def __init__(self, parent, title = None, message = None):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        if message:
            self.message = message
        else:
            self.message = ''

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        self.text = Text(master=self)
        self.text.insert(END, self.message)
        self.text.pack(side=TOP, pady=5, padx=5)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=BOTTOM, pady=5, padx=5)
        #w = Button(box, text="Cancel", width=10, command=self.cancel)
        #w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        #self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override