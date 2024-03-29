#!/usr/bin/env python
# coding: utf-8
# 作者: 韩君太
# QQ: 1669592286

import sys

# Seeing as this can be loaded in either Maya 2016 or 2017,
# the first thing I need to do is check if PySide2 is loaded.
# If it's not, there's no need to make any changes
if "PySide2" in sys.modules:
    # Repath PySide and shiboken so scripts can still call "import PySide"
    # By doing this in the sys.modules I can ensure this is going to affect all my scripts
    # and not just this single one
    sys.modules["PySide"] = sys.modules["PySide2"]
    
    # Shiboken and pyside2uic also needed repathing
    sys.modules["shiboken"] = sys.modules["shiboken2"]
    
    # I bring in pyside2uic to make sure it's in the sys.modules before I repath it
    import pyside2uic
    
    sys.modules["pysideuic"] = sys.modules["pyside2uic"]
    
    # I add entries in the modules dict that point to the new locations...
    sys.modules["PySide.QtGui"] = sys.modules["PySide2.QtGui"]
    sys.modules["PySide.QtCore"] = sys.modules["PySide2.QtCore"]
    
    # Now because all our old scripts will still be looking in QtGui for all the QWidgets
    # I need to merge the new QtWidgets module into the PySide.QtGui module. I do this by
    # using the dictionary.update() method.
    sys.modules["PySide.QtGui"].__dict__.update(sys.modules["PySide2.QtWidgets"].__dict__)
    
    # I found after running some of my tools that anything that used Custom Widgets that had been
    # generated by pyside-uic, that the old flag PySide.QtGui.QApplication.UnicodeUTF8 had been replaced
    # with a simple '-1'.
    # To get around this I used the setattr method (you cannot edit dict_proxy objects,
    # which sys.modules["PySide.QtGui"].QApplication returns as) to replace the flag with -1
    # ensuring that the custom widget still built in PySide2
    import PySide
    from PySide import QtGui, QtCore, QtWidgets
    
    setattr(sys.modules["PySide.QtGui"], "QApplication", sys.modules["PySide2.QtWidgets"].QApplication)
    setattr(sys.modules["PySide.QtGui"].QApplication, "UnicodeUTF8", -1)
    
    # I found a couple more little changes as I went along...
    setattr(sys.modules["PySide.QtGui"], "QSortFilterProxyModel", sys.modules["PySide2.QtCore"].QSortFilterProxyModel)
    setattr(sys.modules["PySide.QtGui"].QHeaderView, "setResizeMode",
            sys.modules["PySide2.QtWidgets"].QHeaderView.setSectionResizeMode)
