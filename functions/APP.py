from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtCore import (
    QPropertyAnimation, QSequentialAnimationGroup, QPoint, QSize, Qt,
    QThread, pyqtSignal, pyqtSlot
)
from speech_recognition import speech_rec
from chat_bot import generate_text
from text_to_speech import talk
# from ImageAnlysis import VideoWidget
import cv2


class ConversationThread(QThread):
    input_signal = pyqtSignal(str)
    output_signal = pyqtSignal(str)
    update_gui_signal = pyqtSignal(str)

    def run(self):    
        while True:
            input_text = speech_rec()
            self.update_gui_signal.emit(input_text)
            output_text = generate_text(input_text)
            self.update_gui_signal.emit(output_text)
            talk(output_text)
            
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("VIRTUAL GUIDE")
        self.setStyleSheet("""
            background-color: #4d4f5c;
        """)
        
        hboxMain = QHBoxLayout(self)
        vbox = QVBoxLayout(self)
        vbox2 = QVBoxLayout(self)
        hbox2 = QHBoxLayout()
        hbox = QHBoxLayout()

        label = QLabel("Hello, I'm your Virtual Guide.")
        label.setStyleSheet("""
            color: #DEDEDE; 
            font-size: 25px; 
            font-family: Helvetica; 
            font-weight: bold; 
            text-align: center;
        """)
        
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setGeometry(0, 0, self.width(), self.height())
        
        self.textEditInput = QTextEdit()
        self.textEditInput.setReadOnly(True)
        self.textEditInput.setMinimumSize(500, 500)
        self.textEditInput.setStyleSheet("""
        QTextEdit {
            border: 1px solid white;
            background-color: black;
            color: white;
            font-size: 20px;
            font-weight: bold;
            font-family: Helvetica;
        }
        """
        )
        
        placeholderbot = QLabel("hej")
        placeholderbot.setMinimumSize(500, 500)
        placeholderbot.setStyleSheet("background-color: white;")
        
        hbox2.addWidget(label)
        hbox2.addStretch(1)
        vbox2.addLayout(hbox2)
        vbox2.addWidget(placeholderbot, 1)
        hbox.addWidget(self.buttonStart())
        hbox.addWidget(self.buttonStop())
        vbox2.addLayout(hbox)
        vbox.addWidget(self.textEditInput)
        hboxMain.addLayout(vbox)
        hboxMain.addLayout(vbox2)

        self.conversation_thread = ConversationThread()
        self.conversation_thread.update_gui_signal.connect(self.set_text)
        
    def buttonStop(self):
        button = QPushButton("KILL ME", self)
        button.setFixedSize(250, 50)
        button.clicked.connect(QApplication.quit)
        button.setStyleSheet("""     
            QPushButton {
                background-color: #1e90ff;
                color: white; 
                font-family: Helvetica;
                border-radius : 10; 
                border : 5px solid #1e90ff;
                font-weight: bold;
                padding: 10px; 
            }
            QPushButton:hover {
                text-decoration: underline;
            } 
        """)         
        return button
     
    def buttonStart(self): 
        button = QPushButton("START CONVERSATION", self)
        button.setFixedSize(250, 50)
        button.clicked.connect(self.on_button_start_clicked)
        button.setStyleSheet(""" 
            QPushButton {
                background-color: #1e90ff;
                color: white; 
                font-family: Helvetica;
                border-radius : 10; 
                border : 5px solid #1e90ff;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                text-decoration: underline;
            } 
        """) 
        return button 
    
    def on_button_start_clicked(self):
        self.textEditInput.setText(self.textEditInput.toPlainText() + "\n\nConversation started, I'm listening..\n\n")
        if not self.conversation_thread.isRunning():
            self.conversation_thread.start()

    def set_text(self, text):
        self.textEditInput.append(text)
    
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()



