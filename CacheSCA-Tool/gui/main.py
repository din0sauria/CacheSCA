import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QFont
import mainwindow as mw

def main():
	app = QApplication(sys.argv)
	w = QMainWindow()
	ui = mw.MainWindow()
	ui.setupUi(w)
	w.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
