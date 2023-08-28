import sys, socket
from threading import Thread
from PyQt5 import QtWidgets, QtCore, uic

class Socket():

    def __init__(self, prnt):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.parent = prnt
        self.connections = []
        self.clientAddresses = []
        serverAddress = ('localhost', 10000)
        self.socket.bind(serverAddress)
        self.socket.listen()

    def accept(self):
        while(True):
            try:
                connection, clientAddress = self.socket.accept()
                self.connections.append(connection)
                self.clientAddresses.append(clientAddress)
                connection.send(('Вы ' + str(len(self.connections)) + '-й в очереди!').encode())
                self.parent.addCheck()
            except BaseException:
                break

    def receive(self):
        try:
            connection = self.connections[len(self.connections) - 1]
            self.parent.window.upd()
            connection.recv(16)
            index = self.connections.index(connection)
            connection.send(('close').encode())
            self.connections.pop(index)
            self.clientAddresses.pop(index)
            for ind in range(len(self.connections), index, -1):
                self.connections[ind - 1].send(('Вы ' + str(ind) + '-й в очереди!').encode())
            self.parent.thread3.pop(index)
            self.parent.window.upd()
        except BaseException:
            pass

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('MainWindow.ui', self)
        self.parent = parent
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.waitDialUpdate)
        self.heroNumber.addItem('Билли Бонс')
        self.heroNumber.addItem('Капитан Смоллетт')
        self.heroNumber.addItem('Доктор Ливси')
        self.heroNumber.addItem('Сквайр Трелони')
        self.heroNumber.addItem('Чёрный пёс')
        self.heroNumber.addItem('Джон Сильвер')
        self.heroNumber.addItem('Другие пираты')
        self.sendButton.clicked.connect(self.sendButtonPushed)
        self.clientQueue.setEnabled(False)
        self.clientQueue.setMinimum(1)
        self.clientQueue.setMaximum(1)
        self.sendButton.setVisible(False)
        self.sendButton.setEnabled(False)
        self.waitLabel.setVisible(True)
        self.waitDial.setVisible(True)
        self.timer.start()
        self.parent.thread2 = Thread(target=self.parent.socket.accept)
        self.parent.thread2.start()

    def upd(self):
        if len(self.parent.socket.connections) > 0:
            self.clientQueue.setEnabled(True)
            self.clientQueue.setMaximum(len(self.parent.thread3))
            self.sendButton.setVisible(True)
            self.sendButton.setEnabled(True)
            self.waitLabel.setVisible(False)
            self.waitDial.setVisible(False)
        else:
            self.clientQueue.setMaximum(1)
            self.clientQueue.setEnabled(False)
            self.sendButton.setVisible(False)
            self.sendButton.setEnabled(False)
            self.waitLabel.setVisible(True)
            self.waitDial.setVisible(True)

    def sendButtonPushed(self):
        self.parent.send()

    def waitDialUpdate(self):
        self.waitDial.setValue(0) if self.waitDial.value() == 100 else self.waitDial.setValue(self.waitDial.value() + 1)

    def closeEvent(self, ev):
        if len(self.parent.socket.connections) != 0:
            messsageBox = QtWidgets.QMessageBox()
            messsageBox.setWindowTitle('Предупреждение')
            messsageBox.setText('Сервер соединён с несколькими клиентами!\n'
                                'Вы действительно хотите остановить работу сервера?')
            messsageBox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            messsageBox.addButton('Да', 5)
            messsageBox.addButton('Нет', 6)
            reply = messsageBox.exec()
            if reply == 1:
                ev.ignore()
            elif reply == 0:
                ev.accept()
        else:
            ev.accept()
        for ind in range(len(self.parent.thread3), 0, -1):
            self.parent.socket.connections[ind - 1].send(('stop').encode())
        self.parent.socket.socket.close()
        self.parent.socket.connections = None
        self.parent.socket.clientAddresses = None
        self.parent.thread3 = None

class Server(QtCore.QObject):

    def __init__(self):
        super().__init__()
        self.thread1 = Thread(target=self.startApp)
        self.thread1.start()
        self.socket = Socket(self)
        self.thread3 = []

    def addCheck(self):
        thr = Thread(target=self.socket.receive)
        self.thread3.append(thr)
        self.thread3[len(self.thread3) - 1].start()

    def startApp(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow(parent=self)
        self.window.show()
        sys.exit(self.app.exec_())

    def send(self):
        self.socket.connections[self.window.clientQueue.value() - 1].send(
            str(self.window.heroNumber.currentIndex()).encode())

if __name__ == '__main__':
    server = Server()