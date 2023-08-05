#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

from .view import WXView


class WXViewer(wx.App):
    """Simple graphics viewer application."""
    
    
    def OnInit(self):
        """Init application."""
        
        # init frame
        self._frame = WXViewFrame(None, -1, 'Pero')
        
        # show frame
        self.SetTopWindow(self._frame)
        try: wx.Yield()
        except: pass
        
        return True
    
    
    def set_size(self, size):
        """
        Sets app window size.
        
        Args:
            size: (float, float)
                App window size as (width, height).
        """
        
        self._frame.SetClientSize(size)
        self._frame.Centre(wx.BOTH)
    
    
    def set_title(self, title):
        """
        Sets app window title.
        
        Args:
            title: str
                App window title.
        """
        
        self._frame.SetTitle(title or "")
    
    
    def set_graphics(self, graphics):
        """
        Sets graphics to draw.
        
        Args:
            graphics: pero.WXView or pero.Graphics
        """
        
        self._frame.set_graphics(graphics)
    
    
    def show(self):
        """Shows app."""
        
        self.MainLoop()
    
    
    def refresh(self):
        """Redraws graphics."""
        
        self._frame.refresh()


class WXViewFrame(wx.Frame):
    """Main application frame."""
    
    
    def __init__(self, parent, id, title, size=(750, 500), style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE):
        
        wx.Frame.__init__(self, parent, -1, title, size=size, style=style)
        self.SetBackgroundColour((255, 255, 255))
        
        # init panel
        self._panel = wx.Panel(self, -1, style=wx.WANTS_CHARS)
        self._panel.SetSizer(wx.BoxSizer(wx.VERTICAL))
        
        # init view
        self._view = None
        
        # show frame
        self.Layout()
        self.Centre(wx.BOTH)
        self.Show(True)
        self.SetMinSize((100, 100))
    
    
    def set_graphics(self, graphics):
        """
        Sets graphics to draw.
        
        Args:
            graphics: pero.WXView or pero.Graphics
        """
        
        # init view
        if isinstance(graphics, WXView):
            self._view = graphics
        else:
            self._view = WXView(self._panel)
            self._view.graphics = graphics
        
        # clean sizer
        self._panel.Sizer.Clear(True)
        
        # add to sizer
        self._panel.Sizer.Add(self._view, 1, wx.EXPAND)
        self._panel.Sizer.Layout()
    
    
    def refresh(self):
        """Redraws graphics."""
        
        if self._view is not None:
            self._view.refresh()
