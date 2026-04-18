from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog
import typing
import qfluentwidgets as qfw

class FileFolderSelector(QWidget):
	selectedSignal = pyqtSignal()

	def __init__(self, parent=None, button_text: str = 'Browse',
			                        file_dialog: typing.Callable = QFileDialog.getOpenFileName,
									*args, **kwargs):
		super().__init__(parent)

		self.file_dialog = file_dialog
		self.args = args
		self.kwargs = kwargs

		self.is_multi = bool(file_dialog == QFileDialog.getOpenFileNames)
		self.results = [] if self.is_multi else ''

		self.lineEdit = qfw.LineEdit(self)
		self.lineEdit.setReadOnly(True)
		self.browseButton = qfw.PushButton(button_text, self)
		self.browseButton.clicked.connect(self.onBrowseButtonClicked)

		self.layout = QHBoxLayout(self)
		self.layout.addWidget(self.lineEdit)
		self.layout.addWidget(self.browseButton)

	# --------------- Methods ---------------
	def getFilePath(self):
		return self.results
	
	def clear(self):
		self.lineEdit.clear()
		self.results = [] if self.is_multi else ''

	def setButtonText(self, text: str):
		self.browseButton.setText(text)

	def setFileDialog(self, file_dialog: typing.Callable, *args, **kwargs):
		self.file_dialog = file_dialog
		self.args = args
		self.kwargs = kwargs

		self.is_multi = bool(file_dialog == QFileDialog.getOpenFileNames)
		self.results = [] if self.is_multi else ''
	
	def setEnabled(self, enabled: bool):
		super().setEnabled(enabled)
		self.lineEdit.setEnabled(enabled)
		self.browseButton.setEnabled(enabled)

	# --------------- Slots ---------------
	def onBrowseButtonClicked(self):
		filePath, _ = self.file_dialog(self, *self.args, **self.kwargs)

		if not filePath:
			return

		self.results = filePath

		if self.is_multi:
			self.lineEdit.setText('; '.join(self.results))
		else:
			self.lineEdit.setText(self.results)

		self.selectedSignal.emit()