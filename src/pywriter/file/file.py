"""Provide a generic class for yWriter project representation.

All classes representing specific file formats inherit from this class.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from urllib.parse import quote
import os
from pywriter.pywriter_globals import *


class File:
    """Abstract yWriter project file representation.

    This class represents a file containing a novel with additional 
    attributes and structural information (a full set or a subset
    of the information included in an yWriter project file).

    Public methods:
        read() -- Parse the file and get the instance variables.
        write() -- Write instance variables to the file.

    Public instance variables:
        projectName -- str: URL-coded file name without suffix and extension. 
        projectPath -- str: URL-coded path to the project directory. 
        filePath -- str: path to the file (property with getter and setter). 
    """
    DESCRIPTION = _('File')
    EXTENSION = None
    SUFFIX = None
    # To be extended by subclass methods.

    _PRJ_KWVAR = []
    _CHP_KWVAR = []
    _SCN_KWVAR = []
    _CRT_KWVAR = []
    _LOC_KWVAR = []
    _ITM_KWVAR = []
    _PNT_KWVAR = []
    # Keyword variables for custom fields in the .yw7 XML file.

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.

        Positional arguments:
            filePath -- str: path to the file represented by the File instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.  
            
        Extends the superclass constructor.          
        """
        super().__init__()
        self.novel = None

        self._filePath = None
        # str
        # Path to the file. The setter only accepts files of a supported type as specified by EXTENSION.

        self.projectName = None
        # str
        # URL-coded file name without suffix and extension.

        self.projectPath = None
        # str
        # URL-coded path to the project directory.

        self.filePath = filePath

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath):
        """Setter for the filePath instance variable.
                
        - Format the path string according to Python's requirements. 
        - Accept only filenames with the right suffix and extension.
        """
        if self.SUFFIX is not None:
            suffix = self.SUFFIX
        else:
            suffix = ''
        if filePath.lower().endswith(f'{suffix}{self.EXTENSION}'.lower()):
            self._filePath = filePath
            head, tail = os.path.split(os.path.realpath(filePath))
            self.projectPath = quote(head.replace('\\', '/'), '/:')
            self.projectName = quote(tail.replace(f'{suffix}{self.EXTENSION}', ''))

    def read(self):
        """Parse the file and get the instance variables.
        
        Raise the "Error" exception in case of error. 
        This is a stub to be overridden by subclass methods.
        """
        raise Error(f'Read method is not implemented.')

    def write(self):
        """Write instance variables to the file.
        
        Raise the "Error" exception in case of error. 
        This is a stub to be overridden by subclass methods.
        """
        raise Error(f'Write method is not implemented.')

    def _convert_to_yw(self, text):
        """Return text, converted from source format to yw7 markup.
        
        Positional arguments:
            text -- string to convert.
        
        This is a stub to be overridden by subclass methods.
        """
        return text.rstrip()

    def _convert_from_yw(self, text, quick=False):
        """Return text, converted from yw7 markup to target format.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick -- bool: if True, apply a conversion mode for one-liners without formatting.
        
        This is a stub to be overridden by subclass methods.
        """
        return text.rstrip()

