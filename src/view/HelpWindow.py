import os
from PySide2 import QtCore
from PySide2.QtWebEngineWidgets import QWebEngineView


web_view: QWebEngineView = None


def show_help():
    global web_view
    if web_view is not None:
        web_view.close()
    web_view = QWebEngineView()
    # paths need to be absolute, therefore calculate realtive to current file
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Help_en.html"))
    url = QtCore.QUrl.fromLocalFile(path)
    web_view.load(url)
    web_view.setWindowTitle("Help")
    web_view.show()
