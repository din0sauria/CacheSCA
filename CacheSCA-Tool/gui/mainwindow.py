from ui.mainwindow_ui import Ui_MainWindow

import qfluentwidgets as qfw

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QFont
import subprocess

import numpy as np

class Ui_Base(Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.target = 'original'
		self.cipher = 'AES'
		self.aim    = 'original'

	def setupUi(self, MainWindow):
		super().setupUi(MainWindow)

		# MainWindow Style
		self.MainWindow = MainWindow
		MainWindow.setFixedSize(MainWindow.size())
		MainWindow.setWindowIcon(qfw.FluentIcon.FINGERPRINT.icon()) # TODO
		MainWindow.setWindowTitle('CacheSCA-Tool') # TODO

		# Page Selector
		self.stackedWidget.setCurrentIndex(0)

		self.pivot = qfw.Pivot(self.centralwidget)
		self.pivot.addItem(
			routeKey='Home',
			text='Home',
			icon=qfw.FluentIcon.HOME,
			onClick=lambda: self.stackedWidget.setCurrentIndex(0)
		)
		self.pivot.addItem(
			routeKey='Performance',
			text='Performance',
			icon=qfw.FluentIcon.SPEED_HIGH,
			onClick=lambda: self.stackedWidget.setCurrentIndex(1)
		)
		self.pivot.addItem(
			routeKey='Evaluation',
			text='Evaluation',
			icon=qfw.FluentIcon.VPN,
			onClick=lambda: self.stackedWidget.setCurrentIndex(2)
		)
		self.pivot.setCurrentItem('Home')

	# --------------- Common Methods ---------------
	def message(self, title: str, content: str):
		w = qfw.MessageBox(title, content, self.MainWindow)
		w.cancelButton.setVisible(False)
		w.exec()

	# --------------- Common Static Methods ---------------
	@staticmethod
	def run_command(command: list, cwd: str):
		print(' '.join(command), cwd)
		try:
			result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
			return True, result.stdout + '\n' + result.stderr
		except subprocess.CalledProcessError as e:
			return False, e.stdout + '\n' + e.stderr
		except Exception as e:
			return False, str(e)

class UI_HomePage(Ui_Base):
	def setupUi(self, MainWindow):
		super().setupUi(MainWindow)

		self.comboBox4Target.currentTextChanged.connect(self.onTargetChanged)
		self.refresh_target_selector()

		self.comboBox4Cipher.addItems(['AES', 'SM4'])
		self.comboBox4Cipher.setCurrentText(self.cipher)
		self.comboBox4Cipher.currentTextChanged.connect(self.onCipherChanged)

		self.selector4Target.setEnabled(False)
		self.selector4Target.selectedSignal.connect(self.onCustomTargetSelected)

		self.update_aim()

	# --------------- Methods ---------------
	def set_target(self, target):
		self.target = target
		self.update_aim()

	def set_cipher(self, cipher):
		self.cipher = cipher
		self.update_aim()
	
	def update_aim(self):
		if self.target == 'original':
			self.aim = f'original'
		else:
			self.aim = f'{self.cipher.lower()}_{self.target}'

	def refresh_target_selector(self):
		self.comboBox4Target.blockSignals(True)
		
		while self.comboBox4Target.count() > 0:
			self.comboBox4Target.removeItem(0)
		
		if self.cipher == 'AES':
			self.comboBox4Target.addItems(['original', 'preload', 'constant_time', 'lut_p', 'custom'])
		elif self.cipher == 'SM4':
			self.comboBox4Target.addItems(['original', 'preload', 'lut_p', 'custom'])
			if self.target == 'constant_time':
				self.target = 'original'
		else:
			self.message('Error', 'Unsupported Cipher Selected!')
			return
		
		self.comboBox4Target.setCurrentText(self.target)

		self.comboBox4Target.blockSignals(False)
	# --------------- Slots ---------------
	def onTargetChanged(self, text):
		if text == 'custom':
			self.set_target('custom')
			self.selector4Target.setEnabled(True)
		else:
			self.set_target(text)
			self.selector4Target.setEnabled(False)
	
	def onCipherChanged(self, text):
		self.set_cipher(text)
		self.refresh_target_selector()

	def onCustomTargetSelected(self):
		filepath = self.selector4Target.getFilePath()
		self.run_command(['cp', filepath, f'./hitls/custom/libhitls_crypto.so'], cwd='.')

class UI_PerformancePage(Ui_Base):
	def setupUi(self, MainWindow):
		super().setupUi(MainWindow)

		self.comboBox4Testdata.addItems(['built-in', 'custom'])
		self.comboBox4Testdata.setCurrentText('built-in')
		self.comboBox4Testdata.currentTextChanged.connect(self.onTestdataChanged)

		self.selector4Testdata.setEnabled(False)

		self.pushButton4Test.clicked.connect(self.onStartPerformanceTest)
		self.pushButton4Testsave.clicked.connect(self.onSavePerformanceResult)

		self.selector4Testcmp.setFileDialog(QFileDialog.getOpenFileNames, 'Select Comparison Files', '', 'All Files (*)')
		self.selector4Testcmp.selectedSignal.connect(self.onComparisonFileSelected)

		self.pushButton4Testclear.clicked.connect(self.onClearComparisonData)

		self.chart_init()

	# --------------- Methods ---------------
	def chart_init(self):
		self.ax_categories = ['Low', 'Medium', 'High', 'Extreme']
		self.ax_data = {
			'Current': [0] * len(self.ax_categories)
		}

		self.ax = self.chart4Testcmp.figure.subplots()
		self.ax_x = np.arange(len(self.ax_categories))

	def chart_draw(self):
		self.ax.clear()
		
		if not self.ax_data:
			self.chart4Testcmp.draw()
			return

		self.ax_width = 0.5 / len(self.ax_data)

		for i, (key, value) in enumerate(self.ax_data.items()):
			bars = self.ax.bar(self.ax_x + i * self.ax_width, value, self.ax_width,
					 label=key,
					 alpha=0.8, edgecolor='black')
		
			for bar in bars:
				height = bar.get_height()
				self.ax.text(bar.get_x() + bar.get_width()/2, height + 2,
					f'{height}', ha='center', va='bottom', fontweight='bold')
		
		self.ax.set_title('', fontsize=16, fontweight='bold') # TODO
		self.ax.set_xlabel('', fontsize=12)
		self.ax.set_ylabel('', fontsize=12)
		self.ax.set_xticks(self.ax_x + self.ax_width * (len(self.ax_data) - 1) / 2)
		self.ax.set_xticklabels(self.ax_categories)
		self.ax.grid(axis='y', alpha=0.3)
		self.ax.legend()
		self.ax.figure.tight_layout()

		self.chart4Testcmp.draw()

	def payload(self, datafile: str, level: str, cwd: str):
		cmd = ['python3', f'payload.py', self.aim, self.cipher, datafile, level]
		
		success, output = self.run_command(cmd, cwd=cwd)
		if not success:
			self.message('Error', f'Performance Test Failed!\n\n{output}')
			return None
		
		return int(output.strip())
	# --------------- Static Methods ---------------
	@staticmethod
	def read_performance_result(filepath: str):
		with open(filepath, 'r') as f:
			try:
				data = f.readlines()[0].strip().split(' ')
				return list(map(int, data))
			except:
				return []

	# --------------- Slots ---------------
	def onTestdataChanged(self, text):
		if text == 'custom':
			self.selector4Testdata.setEnabled(True)
		else:
			self.selector4Testdata.setEnabled(False)
	
	def onStartPerformanceTest(self):
		if self.comboBox4Testdata.currentText() == 'custom':
			if not self.selector4Testdata.getFilePath():
				self.message('Info', 'Please select a custom test data file.')
				return
			datafile = self.selector4Testdata.getFilePath()
		else:
			datafile = 'data'
		
		for i, level in enumerate(self.ax_categories):
			result = self.payload(datafile, level.lower(), cwd='./payload')
			self.ax_data['Current'][i] = result if result else 0
		
		self.chart_draw()

	def onSavePerformanceResult(self):
		filepath, _ = QFileDialog.getSaveFileName(self.MainWindow, 'Save Performance Result', '', 'All Files (*)')
		if not filepath:
			return
		with open(filepath, 'w') as f:
			f.write(' '.join(map(str, self.ax_data['Current'])))

	def onComparisonFileSelected(self):
		files = self.selector4Testcmp.getFilePath()

		for file in files:
			filename = file.replace('\\', '/').split('/')[-1].split('.')[0]
			data = self.read_performance_result(file)
			if data:
				self.ax_data[filename] = data
			else:
				self.message('Error', f'Failed to read performance data from file: {file}')
		
		self.chart_draw()
	
	def onClearComparisonData(self):
		self.ax_data.clear()
		self.chart_draw()

class UI_EvaluationPage(Ui_Base):
	def setupUi(self, MainWindow):
		super().setupUi(MainWindow)

		self.spinBox4Eva.setMinimum(100)
		self.spinBox4Eva.setMaximum(10000)
		self.spinBox4Eva.setSingleStep(100)
		self.spinBox4Eva.setValue(1000)

		self.pushButton4Eva.clicked.connect(self.onStartEvaluation)

		self.pager4Eva.setEnabled(True)
		self.pager4Eva.setVisibleNumber(4)
		self.pager4Eva.setNextButtonDisplayMode(qfw.PipsScrollButtonDisplayMode.ALWAYS)
		self.pager4Eva.setPreviousButtonDisplayMode(qfw.PipsScrollButtonDisplayMode.ALWAYS)
		self.pager4Eva.currentIndexChanged.connect(self.onHeatmapPageChanged)

		self.heatmap_init()
	
	# --------------- Methods ---------------
	def heatmap_init(self):
		pass
	
	def heatmap(self, data: np.ndarray, rows: list, set_idx: np.ndarray):
		import seaborn as sns
		import pandas as pd

		self.chart4Eva.figure.clear()
		self.heatmap_ax = self.chart4Eva.figure.add_subplot(111)

		rows_str = [f'0x{r:02X}' for r in rows]
		df = pd.DataFrame(data[rows], index=rows_str)

		rank_df = df.rank(axis=1, ascending=False, method='dense').astype(int)

		annot_matrix = np.full(df.shape, "", dtype=object)
		for i in range(len(df)):
			for j in range(len(df.columns)):
				rk = rank_df.iloc[i, j]
				
				if rk < 10:
					annot_matrix[i, j] = ''# f'{rk}'
				
				if j == set_idx[rows[i]]:
					annot_matrix[i, j] += '*'

		sns.heatmap(df, ax=self.heatmap_ax, annot=annot_matrix, fmt="", cmap="viridis", cbar=True)

		self.heatmap_ax.set_xlabel("Cache Set Index")
		self.heatmap_ax.set_ylabel("Plaintext Byte Value")
		self.heatmap_ax.set_title("Cache Access Heatmap")
		self.chart4Eva.draw()

	def analyze_evaluation_result(self, filepath: str):
		self.raw_data = np.zeros((16, 256, 64), dtype=int)
		self.valid_rows = []
		
		with open(filepath, "r") as f:
			for line in f:
				parts = line.strip().split(": ")
				if len(parts) != 2:
					continue

				idx, pt = parts[0].split()
				idx = int(idx)
				pt = int(pt, 16)

				values = list(map(int, parts[1].split()))

				self.raw_data[idx, pt] = np.array(values)

				if idx == 0:
					self.valid_rows.append(pt)

		self.skey = b''
		self.cache_set_idx = [None] * 16
		for i in range(16):
			keybyte, _, set_idx, _ = self.analyze(self.raw_data[i], self.valid_rows)

			self.skey += keybyte.to_bytes(1, 'big')
			self.cache_set_idx[i] = set_idx

	def set_skey(self):
		skey_str = ''.join([f'{(b&0x0F):1X}-' for b in self.skey])
		self.label4Eva.setText('[Res] ' + skey_str)
	
	def set_heatmap(self, idx: int):
		self.heatmap(self.raw_data[idx], self.valid_rows, self.cache_set_idx[idx])

	def set_pager(self, pages: int):
		self.pager4Eva.setPageNumber(pages)
		self.pager4Eva.setCurrentIndex(0)
		self.pager4Eva.setEnabled(True)

	def evaluate(self, skey_str: str, samples: int, cwd: str, fout: str):
		if not skey_str:
			skey_str = '0b7e151628aed2a6abf7158809cf4f3c'

		cmd = ['make', f'run-{self.cipher.lower()}-{self.aim}',
			   'ARGS=\"-k {} -s {}\"'.format(skey_str.lower(), samples),
			   '>', fout]
		
		success, output = self.run_command(cmd, cwd=cwd)
		if not success:
			self.message('Error', f'Evaluation Failed!\n\n{output}')
			return False
		
		return True

	# --------------- Static Methods ---------------
	@staticmethod
	def analyze(data: np.ndarray, rows: list):
		maxn = -np.inf
		keybyte = -1
		offset = -1

		for guess in range(16):
			for off in range(64):
				sum = 0
				for pt in rows:
					set_idx = (off + ((pt >> 4) ^ guess)) % 64
					sum += data[pt, set_idx]

				if sum > maxn:
					maxn = sum
					keybyte = guess
					offset = off
		
		set_idx = np.zeros(256, dtype=int)
		for pt in rows:
			set_idx[pt] = (offset + ((pt >> 4) ^ keybyte)) % 64
		
		return keybyte, offset, set_idx, maxn

	@staticmethod
	def is_key_valid(skey_str: str):
		if len(skey_str) == 0:
			return True

		try:
			skey_bytes = bytes.fromhex(skey_str)
			return len(skey_bytes) == 16
		except:
			return False

	# --------------- Slots ---------------
	def onStartEvaluation(self):
		skey_str = self.lineEdit4Eva.text().strip()
		if not self.is_key_valid(skey_str):
			self.message('Error', 'Invalid Secret Key Format! Please input a hexadecimal string of 16 bytes.')
			return

		cwd = './evaluation'
		fout = 'result'
		_ = self.evaluate(skey_str, self.spinBox4Eva.value(), cwd=cwd, fout=fout)

		self.analyze_evaluation_result(f'{cwd}/{fout}')
		self.set_skey()
		self.set_heatmap(0)
		self.set_pager(16 if self.cipher == 'AES' else 4)

	def onHeatmapPageChanged(self, index: int):
		self.text4Eva.setText(f'Byte Index: {index}')
		self.set_heatmap(index)

class MainWindow(UI_HomePage, UI_PerformancePage, UI_EvaluationPage):
	def setupUi(self, MainWindow):
		return super().setupUi(MainWindow)
