import sys, socket, winsound, random
from threading import Thread
from PyQt5 import QtWidgets, QtCore, uic

class Socket():

    def __init__(self, prnt):
        self.parent = prnt
        self.serverAddress = ('localhost', 10000)

    def receive(self):
        while(True):
            try:
                if self.serverAddress == (None, None):
                    break
                self.data = None
                self.parent.window.informLabel.setText('Ожидание соединения с сервером!')
                self.parent.window.waitDial.setVisible(True)
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect(self.serverAddress)
                while(True):
                    try:
                        self.data = self.socket.recv(32)
                        mess = self.data.decode()
                        self.parent.window.waitDial.setVisible(False)
                        if mess == '0':
                            winsound.PlaySound('waves\\0\\' + str(random.randint(0, 2)) + '.wav', winsound.SND_ASYNC)
                            self.parent.window.signalList.insertItem(self.parent.window.signalList.count(),
                                                                     'Билли Бонс')
                            continue
                        elif mess == '1':
                            winsound.PlaySound('waves\\1\\' + str(random.randint(0, 5)) + '.wav', winsound.SND_ASYNC)
                            self.parent.window.signalList.insertItem(self.parent.window.signalList.count(),
                                                                     'Капитан Смоллетт')
                            continue
                        elif mess == '2':
                            winsound.PlaySound('waves\\2\\' + str(random.randint(0, 2)) + '.wav', winsound.SND_ASYNC)
                            self.parent.window.signalList.insertItem(self.parent.window.signalList.count(),
                                                                     'Доктор Ливси')
                            continue
                        elif mess == '3':
                            winsound.PlaySound('waves\\3\\' + str(random.randint(0, 1)) + '.wav', winsound.SND_ASYNC)
                            self.parent.window.signalList.insertItem(self.parent.window.signalList.count(),
                                                                     'Сквайр Трелони')
                            continue
                        elif mess == '4':
                            winsound.PlaySound('waves\\4\\' + str(random.randint(0, 1)) + '.wav', winsound.SND_ASYNC)
                            self.parent.window.signalList.insertItem(self.parent.window.signalList.count(),
                                                                     'Чёрный пёс')
                            continue
                        elif mess == '5':
                            winsound.PlaySound('waves\\5\\' + str(random.randint(0, 3)) + '.wav', winsound.SND_ASYNC)
                            self.parent.window.signalList.insertItem(self.parent.window.signalList.count(),
                                                                     'Джон Сильвер')
                            continue
                        elif mess == '6':
                            winsound.PlaySound('waves\\6\\' + str(random.randint(0, 3)) + '.wav', winsound.SND_ASYNC)
                            self.parent.window.signalList.insertItem(self.parent.window.signalList.count(),
                                                                     'Другие пираты')
                            continue
                        elif mess == 'close':
                            self.serverAddress = (None, None)
                            pass
                        elif mess == 'stop':
                            pass
                        else:
                            self.parent.window.informLabel.setText(mess)
                            continue
                        break
                    except BaseException:
                        self.parent.window.informLabel.setText('Ожидание соединения с сервером!')
                        break
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
        self.informLabel.setText('Ожидание соединения с сервером!')
        self.timer.start()

    def waitDialUpdate(self):
        self.waitDial.setValue(0) if self.waitDial.value() == 100 else self.waitDial.setValue(self.waitDial.value() + 1)

    def closeEvent(self, ev):
        if self.parent.socket.data is not None:
            messsageBox = QtWidgets.QMessageBox()
            messsageBox.setWindowTitle('Предупреждение')
            messsageBox.setText('Подключение к серверу установлено!\n'
                                'Вы действительно хотите остановить работу клиента?')
            messsageBox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            messsageBox.addButton('Да', 5)
            messsageBox.addButton('Нет', 6)
            reply = messsageBox.exec()
            if reply == 1:
                ev.ignore()
            elif reply == 0:
                ev.accept()
                self.parent.socket.socket.send(('close').encode())
        else:
            ev.accept()
            self.parent.socket.serverAddress = (None, None)

class Client(QtCore.QObject):

    def __init__(self):
        super().__init__()
        self.thread1 = Thread(target=self.startApp)
        self.thread2 = Thread(target=self.connect)
        self.thread1.start()

    def connect(self):
        self.socket = Socket(self)
        self.socket.receive()

    def startApp(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = MainWindow(parent=self)
        self.window.show()
        self.thread2.start()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    client = Client()