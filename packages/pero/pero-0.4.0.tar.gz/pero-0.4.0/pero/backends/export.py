#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import os.path
from ..enums import *


def export(graphics, path, width=750, height=500, **options):
    """
    Draws given graphics into specified image file using the format determined
    automatically from the file extension. This method makes sure appropriate
    backend canvas is created and provided to graphics 'draw' method.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        path: str
            Full path of a file to save the image into.
        
        width: float
            Image width in device units.
        
        height: float
            Image height in device units.
        
        options: str:any pairs
            Additional parameters for specific backend.
    """
    
    # get filename and extension
    dirname, filename = os.path.split(path)
    basename, extension = os.path.splitext(filename)
    extension = extension.lower()
    
    # get backend
    backend = None
    for module in EXPORT_PRIORITY:
        
        # check if format is recognized by backend
        if extension not in EXPORT_FORMATS[module]:
            continue
        
        # try to import backend
        try:
            if module == BACKEND.JSON:
                from . import json as backend
            
            if module == BACKEND.SVG:
                from . import svg as backend
            
            elif module == BACKEND.QT:
                from . import qt as backend
            
            elif module == BACKEND.WX:
                from . import wx as backend
            
            elif module == BACKEND.CAIRO:
                from . import cairo as backend
            
            elif module == BACKEND.MUPDF:
                from . import mupdf as backend
            
            elif module == BACKEND.PYTHONISTA:
                from . import pythonista as backend
            
            break
        
        # ignore missing library
        except ImportError:
            backend = None
            pass
    
    # unsupported format
    if backend is None:
        message = "Unsupported image format or missing library! -> %s" % extension
        raise NotImplementedError(message)
    
    # export image
    backend.export(graphics, path, width, height, **options)


def show(graphics, title=None, width=750, height=500):
    """
    Shows given graphics in available viewer app. Currently this is only
    available if wxPython is installed or within Pythonista app on iOS. This
    method makes sure appropriate backend canvas is created and provided to
    graphics 'draw' method.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        title: str or None
            Viewer frame title.
        
        width: float
            Image width in device units.
        
        height: float
            Image height in device units.
    """
    
    # show in Qt viewer
    try:
        from . import qt
        qt.show(graphics, title, width, height)
        return
    except ImportError:
        pass
    
    # show in WX viewer
    try:
        from . import wx
        wx.show(graphics, title, width, height)
        return
    except ImportError:
        pass
    
    # show in Pythonista console
    try:
        from . import pythonista
        pythonista.show(graphics, width, height)
        return
    except ImportError:
        pass
    
    # no viewer
    raise ImportError("No viewer available (wxPython or Pythonista needed).")


def debug(graphics, canvas='wx', title="", width=750, height=500, **options):
    """
    Renders given graphics using simple viewer or file format. This method makes
    sure appropriate backend canvas is created and provided to graphics 'draw'
    method. In case of the image export the file is stored in current working
    directory using 'test' and appropriate format as the name.
    
    Args:
        graphics: pero.Graphics
            Graphics to be drawn.
        
        canvas: str
            Specifies drawing mechanism to be used. This can be either 'show',
            'wx' or 'pythonista' to display graphics within a simple viewer app,
            or any of the supported image formats (e.g. 'png', 'svg') to draw
            to 'test.?' file.
        
        title: str or None
            Viewer frame title.
        
        width: float
            Image or viewer width in device units.
        
        height: float
            Image or viewer
        
        options: key:value pairs
            Additional parameters for specific backend.
    """
    
    # render graphics in available viewer
    if canvas == 'show':
        show(graphics, title, width, height)
    
    # render graphics into qt viewer
    elif canvas == 'qt':
        from . import qt
        qt.show(graphics, title, width, height)
    
    # render graphics into wx viewer
    elif canvas == 'wx':
        from . import wx
        wx.show(graphics, title, width, height)
    
    # render graphics into Pythonista console
    elif canvas == 'pythonista':
        from . import pythonista
        pythonista.show(graphics, width, height)
    
    # render graphics as image file
    else:
        filename = "test.%s" % canvas
        export(graphics, filename, width, height, **options)
