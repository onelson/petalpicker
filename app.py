import sys, os, logging, uuid
from cStringIO import StringIO
import pil

from PyQt4.QtCore import (Qt, QObject, QBuffer, QByteArray, QIODevice, QString, QFileInfo, QRect, QRectF, QSize, SIGNAL)
from PyQt4.QtGui import (QApplication, QImage, QDialog, QFileDialog, QGraphicsView, 
                         QGraphicsScene, QPainter, QHBoxLayout, QVBoxLayout, 
                         QPushButton, QPixmap, QGraphicsPixmapItem, 
                         QMessageBox, QMatrix, QGraphicsRectItem)

logging.getLogger().setLevel(logging.DEBUG)
DIRTY = False
PIX = None
class GraphicsView(QGraphicsView):
    
    rubber_band = None
    selection = None
    
    def __init__(self, scene, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setScene(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        
    def wheelEvent(self, event):
        factor = 1.41 ** (-event.delta() / 240.0)
        self.scale(factor, factor)
        
    def __mousePressEvent(self,event):
        self.drag_start = event.pos()
    def __mouseReleaseEvent(self,event):
        global PIX
        self.drag_stop = event.pos()
        im = PIX.pixmap().toImage()
        
        start, stop = self.mapToScene(self.drag_start),self.mapToScene(self.drag_stop)
        logging.debug((start,stop))
        rect = QRectF(start,stop).normalized()

        pix_rect = PIX.mapToItem(PIX,rect).toPolygon().boundingRect()
        logging.debug(pix_rect)
        
        im = im.copy(pix_rect)
        tempfile = os.path.join(os.getenv('TMP'),str(uuid.uuid4())+'.jpg')
        im.save(tempfile, 'JPEG')
        pil.process(tempfile)
        augmented = QGraphicsPixmapItem(QPixmap(tempfile))
        
        augmented.setOffset(rect.topLeft())
        augmented.setMatrix(QMatrix())
        if None != self.selectbox: self.scene().removeItem(self.selectbox)
        self.selectbox = augmented
        self.scene().addItem(self.selectbox)
        
    def mousePressEvent(self, event):
        self.start = event.pos()
        if not self.rubber_band:
            self.rubber_band = QGraphicsRectItem(None, self.scene())
        self.rubber_band.setRect(self.mapToScene(QRect(self.start,QSize())).boundingRect())
        self.scene().addItem(self.rubber_band)
        logging.info(self.__class__.__name__+' press')
    def mouseMoveEvent(self, event):
        if self.rubber_band:
            self.rubber_band.setRect(self.mapToScene(QRect(self.start,event.pos()).normalized()).boundingRect())
            logging.info(self.__class__.__name__+' move')
    def mouseReleaseEvent(self, event):
        if self.rubber_band:
            self.scene().removeItem(self.rubber_band)
            self.rubber_band = None
        logging.info(self.__class__.__name__+' release')
        
class MainForm(QDialog):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        
        self.filename = QString()
        self.scene = QGraphicsScene(self)
        self.view = GraphicsView(self.scene)

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
        global PIX
        item = QGraphicsPixmapItem(pixmap)
        PIX = item
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