import sys, os, logging

from PyQt4.QtCore import Qt
from PyQt4.QtCore import (QObject, QString, QFileInfo, SIGNAL)
from PyQt4.QtGui import (QApplication, QDialog, QFileDialog, QGraphicsView, 
                         QGraphicsScene, QPainter, QHBoxLayout, QVBoxLayout, 
                         QPushButton, QPixmap, QGraphicsPixmapItem, 
                         QMessageBox, QMatrix, )

logging.getLogger().setLevel(logging.DEBUG)
DIRTY = False

class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        
    def wheelEvent(self, event):
        factor = 1.41 ** (-event.delta() / 240.0)
#        logging.debug(factor)
        self.scale(factor, factor)
    def mousePressEvent(self,event):
        logging.debug(event.pos())
    def mouseReleaseEvent(self,event):
        logging.debug(event.pos())

class MainForm(QDialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        
        self.filename = QString()
        self.view = GraphicsView()
        self.scene = QGraphicsScene(self)

        self.view.setScene(self.scene)
        buttonLayout = QVBoxLayout()
        for text, slot in (
                ("&Open", self.addPixmap),
                ("&Quit", self.accept)):
            button = QPushButton(text)
            self.connect(button, SIGNAL("clicked()"), slot)
            if text == "&Quit":
                buttonLayout.addStretch(1)
            buttonLayout.addWidget(button)
        buttonLayout.addStretch()
        layout = QHBoxLayout()
        layout.addWidget(self.view, 1)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        self.setWindowTitle("Petal Picker")

    def addPixmap(self):
        path = (QFileInfo(self.filename).path()
                if not self.filename.isEmpty() else ".")
        fname = QFileDialog.getOpenFileName(self,
                "Add Pixmap", path,
                "Pixmap Files (*.bmp *.jpg *.png *.xpm)")
        if fname.isEmpty(): return
        self.createPixmapItem(QPixmap(fname))


    def createPixmapItem(self, pixmap, matrix=QMatrix()):
        item = QGraphicsPixmapItem(pixmap)
#        item.setFlags(QGraphicsItem.ItemIsSelectable|
#                      QGraphicsItem.ItemIsMovable)
        item.setMatrix(matrix)
        self.scene.clearSelection()
        
        for i in self.scene.items():
            self.scene.removeItem(i)
        
        self.scene.addItem(item)
        self.view.fitInView(item,Qt.KeepAspectRatio)
        
        
        global DIRTY
        DIRTY = True
        
    def accept(self):
        global DIRTY
        if not DIRTY: QDialog.accept(self)
        if DIRTY:
            if self.confirm(): QDialog.accept(self)
            else: return

    def confirm(self):
        global DIRTY
        if (DIRTY and QMessageBox.question(self,
                            "Really Quit?",
                            "Really Quit?",
                            QMessageBox.Yes|QMessageBox.No) ==
            QMessageBox.Yes): return True
        else: return False

app = QApplication(sys.argv)
form = MainForm()
rect = QApplication.desktop().availableGeometry()
form.resize(int(rect.width() * 0.6), int(rect.height() * 0.9))
form.show()
app.exec_()