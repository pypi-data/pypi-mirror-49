#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from ..enums import *
from .prop import PropertyChangedEvt


class PenChangedEvt(PropertyChangedEvt):
    """
    Defines an event which is fired if any pen-related property was changed.
    """
    
    TYPE = EVENT.PEN_CHANGED


class BrushChangedEvt(PropertyChangedEvt):
    """
    Defines an event which is fired if any brush-related property was changed.
    """
    
    TYPE = EVENT.BRUSH_CHANGED


class TextChangedEvt(PropertyChangedEvt):
    """
    Defines an event which is fired if any text-related property was changed.
    """
    
    TYPE = EVENT.TEXT_CHANGED
