"""Provide a frame with a vertical scrollbar. 

Based on the VerticalScrolledFrame example class shown and discussed here:
https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
https://stackoverflow.com/questions/4066974/scrolling-multiple-tkinter-listboxes-together

Mouse wheel binding as proposed by Bryan Oakley:
https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/yw-table
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform
import tkinter as tk
from tkinter import ttk


class ScrolledWindow(ttk.Frame):
    """A Window for a scrollable table. 
    
    Public instance variables:
        rowTitles -- ttk.Frame for a vertically scrolled column of row titles. 
        columnTitles -- ttk.Frame for a horizontally scrolled row of column titles. 
        display -- ttk.Frame for columns and rows to be displayed and scrolled in both directions.
        
    Use the mouse wheel for vertical scrolling, and <Shift>-mouse wheel for horizontal scrolling.    
    """

    def __init__(self, parent, *args, **kw):

        ttk.Frame.__init__(self, parent, *args, **kw)

        # Scrollbars.
        # Note: For some unknown reason the code for the scrollbars does not work as desired.
        # Therefore it is completely commented out.
        # #scrollY = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.yview)
        # #scrollY.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
        # #scrollX = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.xview)
        # #scrollX.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

        # Left column frame.
        leftColFrame = ttk.Frame(self)
        leftColFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Fixed title column header.
        self.topLeft = ttk.Frame(leftColFrame)
        self.topLeft.pack(anchor=tk.W, fill=tk.X, expand=False)

        #--- Vertically scrollable row titles.
        rowTitlesFrame = ttk.Frame(leftColFrame)
        rowTitlesFrame.pack(fill=tk.BOTH, expand=True)
        self._rowTitlesCanvas = tk.Canvas(rowTitlesFrame, bd=0, highlightthickness=0)
        # #self._rowTitlesCanvas.configure(yscrollcommand=scrollY.set)
        self._rowTitlesCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._rowTitlesCanvas.xview_moveto(0)
        self._rowTitlesCanvas.yview_moveto(0)
        # self._rowTitlesCanvas.bind("<MouseWheel>", self.on_mouse_wheel)

        # Create a frame inside the row titles canvas which will be scrolled with it.
        self.rowTitles = ttk.Frame(self._rowTitlesCanvas)
        self._rowTitlesCanvas.create_window(0, 0, window=self.rowTitles, anchor=tk.NW, tags="self.rowTitles")

        def _configure_rowTitles(event):
            # Update the scrollbars to match the size of the display frame.
            size = (self.rowTitles.winfo_reqwidth(), self.rowTitles.winfo_reqheight())
            self._rowTitlesCanvas.config(scrollregion="0 0 %s %s" % size)

            # Update the display Canvas's width to fit the inner frame.
            if self.rowTitles.winfo_reqwidth() != self._rowTitlesCanvas.winfo_width():
                self._rowTitlesCanvas.config(width=self.rowTitles.winfo_reqwidth())

        self.rowTitles.bind('<Configure>', _configure_rowTitles)

        # Right column frame.
        rightColFrame = ttk.Frame(self)
        rightColFrame.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH, expand=True)

        #--- Horizontally scrollable column titles.
        columnTitlesFrame = ttk.Frame(rightColFrame)
        columnTitlesFrame.pack(fill=tk.X, anchor=tk.NW, expand=False)
        self._columnTitlesCanvas = tk.Canvas(columnTitlesFrame, bd=0, highlightthickness=0)
        # #self._columnTitlesCanvas.configure(xscrollcommand=scrollX.set)
        self._columnTitlesCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._columnTitlesCanvas.xview_moveto(0)
        self._columnTitlesCanvas.yview_moveto(0)

        # Create a frame inside the column titles canvas which will be scrolled with it.
        self.columnTitles = ttk.Frame(self._columnTitlesCanvas)
        self._columnTitlesCanvas.create_window(0, 0, window=self.columnTitles, anchor=tk.NW, tags="self.columnTitles")

        def _configure_columnTitles(event):
            # Update the scrollbars to match the size of the display frame.
            size = (self.columnTitles.winfo_reqwidth(), self.columnTitles.winfo_reqheight())
            self._columnTitlesCanvas.config(scrollregion="0 0 %s %s" % size)

            # Update the display Canvas's width and height to fit the inner frame.
            if self.columnTitles.winfo_reqwidth() != self._columnTitlesCanvas.winfo_width():
                self._columnTitlesCanvas.config(width=self.columnTitles.winfo_reqwidth())
            if self.columnTitles.winfo_reqheight() != self._columnTitlesCanvas.winfo_height():
                self._columnTitlesCanvas.config(height=self.columnTitles.winfo_reqheight())

        self.columnTitles.bind('<Configure>', _configure_columnTitles)

        #--- Vertically and horizontally scrollable display.
        displayFrame = ttk.Frame(rightColFrame)
        displayFrame.pack(fill=tk.BOTH, expand=True)
        self._displayCanvas = tk.Canvas(displayFrame, bd=0, highlightthickness=0)
        # #self._displayCanvas.configure(xscrollcommand=scrollX.set)
        # #self._displayCanvas.configure(yscrollcommand=scrollY.set)
        self._displayCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._displayCanvas.xview_moveto(0)
        self._displayCanvas.yview_moveto(0)

        # Create a frame inside the display canvas which will be scrolled with it.
        self.display = ttk.Frame(self._displayCanvas)
        self._displayCanvas.create_window(0, 0, window=self.display, anchor=tk.NW, tags="self.display")

        def _configure_display(event):
            # Update the scrollbars to match the size of the display frame.
            size = (self.display.winfo_reqwidth(), self.display.winfo_reqheight())
            self._displayCanvas.config(scrollregion="0 0 %s %s" % size)
            if self.display.winfo_reqwidth() != self._displayCanvas.winfo_width():
                # Update the display Canvas's width to fit the inner frame.
                self._displayCanvas.config(width=self.display.winfo_reqwidth())

        self.display.bind('<Configure>', _configure_display)
        if platform.system() == 'Linux':
            # Vertical scrolling
            self._rowTitlesCanvas.bind_all("<Button-4>", self.on_mouse_wheel)
            self._rowTitlesCanvas.bind_all("<Button-5>", self.on_mouse_wheel)
            self._displayCanvas.bind_all("<Button-4>", self.on_mouse_wheel)
            self._displayCanvas.bind_all("<Button-5>", self.on_mouse_wheel)

            # Horizontal scrolling
            self._rowTitlesCanvas.bind_all("<Shift-Button-4>", self.on_mouse_wheel)
            self._rowTitlesCanvas.bind_all("<Shift-Button-5>", self.on_mouse_wheel)
            self._displayCanvas.bind_all("<Shift-Button-4>", self.on_mouse_wheel)
            self._displayCanvas.bind_all("<Shift-Button-5>", self.on_mouse_wheel)
        else:
            # Vertical scrolling
            self._rowTitlesCanvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
            self._displayCanvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

            # Horizontal scrolling
            self._rowTitlesCanvas.bind_all("<Shift-MouseWheel>", self.on_shift_mouse_wheel)
            self._displayCanvas.bind_all("<Shift-MouseWheel>", self.on_shift_mouse_wheel)

    def yview(self, *args):
        self._columnTitlesCanvas.yview(*args)
        self._displayCanvas.yview(*args)

    def xview(self, *args):
        self._rowTitlesCanvas.xview(*args)
        self._displayCanvas.xview(*args)

    def on_mouse_wheel(self, event):
        """Vertical scrolling."""
        if platform.system() == 'Windows':
            self._rowTitlesCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            self._displayCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == 'Darwin':
            self._rowTitlesCanvas.yview_scroll(int(-1 * event.delta), "units")
            self._displayCanvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self._rowTitlesCanvas.yview_scroll(-1, "units")
                self._displayCanvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self._rowTitlesCanvas.yview_scroll(1, "units")
                self._displayCanvas.yview_scroll(1, "units")

    def on_shift_mouse_wheel(self, event):
        """Horizontal scrolling."""
        if platform.system() == 'Windows':
            self._columnTitlesCanvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
            self._displayCanvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == 'Darwin':
            self._columnTitlesCanvas.xview_scroll(int(-1 * event.delta), "units")
            self._displayCanvas.xview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self._columnTitlesCanvas.xview_scroll(-1, "units")
                self._displayCanvas.xview_scroll(-1, "units")
            elif event.num == 5:
                self._columnTitlesCanvas.xview_scroll(1, "units")
                self._displayCanvas.xview_scroll(1, "units")

