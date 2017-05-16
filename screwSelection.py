# coding=utf-8
import sys
import os
import sqlite3
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QGridLayout, QVBoxLayout, QTextEdit, QHBoxLayout


class boltSelection(QMainWindow):
    signal_clearance_hole = pyqtSignal()

    def __init__(self):
        super(boltSelection, self).__init__()

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        mainLayout = QVBoxLayout(self.mainWidget)

        gridOne = QGridLayout()
        gridTwo = QGridLayout()
        hbox = QHBoxLayout()

        for column in range(20):
            gridTwo.setColumnStretch(column, 1)
        for row in range(20):
            gridTwo.setRowStretch(row, 1)

        gridOne.setSpacing(10)  # 设置间距
        # self.setContentsMargins(15, 15, 15, 15)  #设置边距

        self.housingLabel = QLabel('Housing Material')
        self.housingCombo = QComboBox()
        self.sizeLabel = QLabel('Screw Size  M')
        self.sizeCombo = QComboBox(self)
        self.pitchlabel = QLabel('Thread Pitch')
        self.pitchCombo = QComboBox()
        self.jointThicknessLabel = QLabel('Join Thickness')
        self.joinThicknessLineEdit = QLineEdit('')
        self.screwLengthLabel = QLabel('Screw Length')
        self.screwLengthcombo = QComboBox()
        self.pictureLabel = QLabel()
        self.pictureLabel.setPixmap(QPixmap(self.resource_path('screw.png')))
        self.tapLengthLabel = QLabel('Tap Length')
        self.tapLengthLineEdit = QLineEdit()
        self.drillLengthLabel = QLabel('Drill Length')
        self.drillLengthLineEdit = QLineEdit()
        self.inner_material_lineEdit = QLineEdit()
        self.outer_material_lineEdit = QLineEdit()
        self.bottom_material_lineEdit = QLineEdit()
        self.clearanceHoleCombo = QComboBox()
        self.clearanceHoleLineEdit = QLineEdit()
        self.calculateBtn = QPushButton('Calculate')
        self.screw_length_display = QLineEdit('Screw')
        self.join_thk_display = QLineEdit('Cover')
        self.notes = QLabel(
            'Determine tap and drill depth for screws you have select,show clerance hole and tap dirll.')
        self.tap_drill_lb = QLabel('Tap drill')
        self.tap_drill_le = QLineEdit()
        self.thread_minor_diameter_lb = QLabel('Thread Minor Diameter   6H')
        self.thread_minor_diameter_le = QLineEdit()

        self.tap_drill_le.setFixedWidth(80)

        gridOne.addWidget(self.housingLabel, 0, 0)
        gridOne.addWidget(self.housingCombo, 0, 1)
        gridOne.addWidget(self.sizeLabel, 0, 2)
        gridOne.addWidget(self.sizeCombo, 0, 3)
        gridOne.addWidget(self.pitchlabel, 0, 4)
        gridOne.addWidget(self.pitchCombo, 0, 5)
        gridOne.addWidget(self.jointThicknessLabel, 1, 0)
        gridOne.addWidget(self.joinThicknessLineEdit, 1, 1)
        gridOne.addWidget(self.screwLengthLabel, 1, 2)
        gridOne.addWidget(self.screwLengthcombo, 1, 3)
        gridOne.addWidget(self.calculateBtn, 1, 4, 1, 2)

        gridTwo.addWidget(self.pictureLabel, 0, 0, 20, 20)
        gridTwo.addWidget(self.tapLengthLabel, 9, 16)
        gridTwo.addWidget(self.tapLengthLineEdit, 10, 16)
        gridTwo.addWidget(self.drillLengthLabel, 10, 17)
        gridTwo.addWidget(self.drillLengthLineEdit, 11, 17, 1, 2)
        gridTwo.addWidget(self.inner_material_lineEdit, 1, 12, 1, 3)
        gridTwo.addWidget(self.outer_material_lineEdit, 1, 7, 1, 3)
        gridTwo.addWidget(self.bottom_material_lineEdit, 17, 7, 1, 3)
        gridTwo.addWidget(self.clearanceHoleCombo, 6, 16, 1, 2)
        gridTwo.addWidget(self.clearanceHoleLineEdit, 7, 16, 1, 2)
        gridTwo.addWidget(self.screw_length_display, 9, 1, 1, 3)
        gridTwo.addWidget(self.join_thk_display, 7, 3, 1, 2)

        hbox.addWidget(self.tap_drill_lb)
        hbox.addWidget(self.tap_drill_le)
        hbox.addWidget(self.thread_minor_diameter_lb)
        hbox.addWidget(self.thread_minor_diameter_le)
        hbox.addStretch()

        mainLayout.addWidget(self.notes)
        mainLayout.addLayout(gridOne)
        mainLayout.addLayout(gridTwo)
        mainLayout.addLayout(hbox)

        self.resize(self.minimumSizeHint())
        self.setWindowTitle("Drill and Tap Depth For Screw Selected")
        iconpath = self.resource_path('jci.ico')
        self.setWindowIcon(QIcon(iconpath))
        self.show()

        self.joinThicknessLineEdit.editingFinished.connect(self.joinInput)

        # 定义下拉列表框中数据

        # 定义壳体材料
        self.housingCombo.addItems(['Steel', 'Iron', 'Alum Alloy & Brass'])

        # 定义螺钉规格
        self.conn = sqlite3.connect(self.resource_path('screwSelection.db'))
        cursor = self.conn.cursor()
        sql = 'select size from metric_profile group by size'
        cursor.execute(sql)
        rs = cursor.fetchall()
        size = [str(i[0]) for i in rs]  # 列表推导式,形成类似['1','2']的结构
        self.sizeCombo.addItems(size)
        cursor.close()
        self.conn.close()

        # 定义螺距数值
        self.sizeCombo.activated.connect(lambda: self.pitchSeries(self.pitchCombo))

        # 定义螺钉长度列表框中数值
        self.screwLengthcombo.addItems(['2.5', '3', '4', '5', '6', '8', '10', '12', '16', '20', '25', '30', '35', '40', '45', '50', '55',
                                        '60', '65', '70', '80', '90', '100', '110', '120', '130', '140', '150', '160', '180', '200', '220', '240', '260', '300'])

        # 计算螺纹深度和钻孔深度
        self.screwLengthcombo.currentIndexChanged.connect(self.outputData)
        self.joinThicknessLineEdit.textChanged.connect(self.outputData)
        self.sizeCombo.currentIndexChanged.connect(self.outputData)
        self.joinThicknessLineEdit.editingFinished.connect(self.outputData)
        self.pitchCombo.currentIndexChanged.connect(self.outputData)
        self.calculateBtn.clicked.connect(self.outputData)

        # update tap drill and thread minor diameter
        self.pitchCombo.currentIndexChanged.connect(self.update_tap_drill)
        self.sizeCombo.currentIndexChanged.connect(self.update_tap_drill)

        # 定义通孔下拉列表数据
        self.clearanceHoleCombo.addItems(
            ['Middle Fit', 'Loose Fit', 'Close Fit'])
        self.signal_clearance_hole.connect(self.update_clearance_hole)
        self.sizeCombo.currentIndexChanged.connect(
            self.emit_sch) 
        # 当螺钉规格改变,发送信号,去更新通孔值
        self.clearanceHoleCombo.currentIndexChanged.connect(self.emit_sch)
        # 定义周边材料尺寸
        self.sizeCombo.currentIndexChanged.connect(self.update_material)

        # 显示螺栓长度和连接件长度
        self.joinThicknessLineEdit.textChanged.connect(
            self.display_join_thk)
        self.screwLengthcombo.currentIndexChanged.connect(
            self.display_screw_length)



    def joinInput(self):
        self.joinThicknessLineEdit.text()

    def pitchSeries(self, combo):
        try:
            self.conn = sqlite3.connect(
                self.resource_path('screwSelection.db'))
            combo.clear()
            size = self.sizeCombo.currentText()
            cursor = self.conn.cursor()
            sql = "select pitch from metric_profile where size =%s" % size
            cursor.execute(sql)
            rs = cursor.fetchall()
            pitch = [str(i[0]) for i in rs]
            self.pitchCombo.addItems(pitch)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.conn.close()


    def outputData(self):

        # 计算螺纹深度
        tap_depth = self.calculate_tap_depth(self.housingCombo.currentText(), self.sizeCombo.currentText(
        ), self.pitchCombo.currentText(), self.joinThicknessLineEdit.text(), self.screwLengthcombo.currentText())
        self.tapLengthLineEdit.setText(tap_depth)

        # 计算钻深度
        drill_depth = self.calculate_drill_depth(
            tap_depth, self.pitchCombo.currentText())
        self.drillLengthLineEdit.setText(drill_depth)



    def update_tap_drill(self):
        tmp =self.query('tap_drill')
        self.tap_drill_le.setText(tmp)
        tmp = self.query('thread_minor_diameter')
        self.thread_minor_diameter_le.setText(tmp)
           


    def query(self,query_info):
        try:
            conn=sqlite3.connect(self.resource_path('screwSelection.db'))
            cursor= conn.cursor()
            #如果是2.0 变成2,以匹配螺纹规格,例如M20x2
            if self.pitchCombo.currentText() !='':
                tp1=float(self.pitchCombo.currentText())
                if round(tp1)==tp1:
                    tp1=round(tp1)
            tmp='M{}x{}'.format(self.sizeCombo.currentText(),tp1)
            sql = "select %s from metric_profile where thread_designation='%s'"%(query_info,tmp)
            cursor.execute(sql)
            rs=cursor.fetchall()   # return list of tuple
            return str(rs[0][0])   # return a string 
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


    def calculate_tap_depth(self, housingMaterial, screwSize, pitch, join, screwLength):
        screwSize = float(screwSize)
        try:
            if join == '':
                join = 0.0
            pitch = float(pitch)
            join = float(join)
            screwLength = float(screwLength)
            if 1.6 < screwSize <= 10:
                if screwLength <= 16:
                    screwLength_bilateral_tolerance = 0.3
                if 16 < screwLength <= 50:
                    screwLength_bilateral_tolerance = 0.4
                if 50 < screwLength <= 120:
                    screwLength_bilateral_tolerance = 0.7
                if 120 < screwLength <= 200:
                    screwLength_bilateral_tolerance = 1.0
                if screwLength > 200:
                    screwLength_bilateral_tolerance = 2.0
            if 12 <= screwSize <= 20:
                if screwLength <= 16:
                    screwLength_bilateral_tolerance = 0.3
                if 16 < screwLength <= 50:
                    screwLength_bilateral_tolerance = 0.4
                if 50 < screwLength <= 120:
                    screwLength_bilateral_tolerance = 1.0
                if 120 < screwLength <= 200:
                    screwLength_bilateral_tolerance = 1.5
                if screwLength > 200:
                    screwLength_bilateral_tolerance = 2.5
            if screwSize > 20:
                if 16 < screwLength <= 50:
                    screwLength_bilateral_tolerance = 0.7
                if 50 < screwLength <= 120:
                    screwLength_bilateral_tolerance = 1.5
                if 120 < screwLength <= 200:
                    screwLength_bilateral_tolerance = 2.0
                if screwLength > 200:
                    screwLength_bilateral_tolerance = 3.0

            thread_engagement = screwLength - join
            thread_engagement_bilateral_tolerance = screwLength_bilateral_tolerance
            thread_engagement_min = thread_engagement - \
                thread_engagement_bilateral_tolerance
            if housingMaterial == 'Steel' and thread_engagement_min < screwSize:
                self.tapLengthLineEdit.setStyleSheet('background-color:red')
                return 'Lengthen screw'
            if housingMaterial == 'Iron' and thread_engagement_min < 1.5 * screwSize:
                self.tapLengthLineEdit.setStyleSheet('background-color:red')
                return 'Lengthen screw'
            if housingMaterial == 'Alum Alloy & Brass' and thread_engagement_min < 2 * screwSize:
                self.tapLengthLineEdit.setStyleSheet('background-color:red')
                return 'Lengthen screw'
            tap_depth_min = thread_engagement + thread_engagement_bilateral_tolerance + pitch

            # default tap depth bilateral tolerance is 1 mm
            tap_depth_nom = tap_depth_min + 1
            if tap_depth_nom > round(tap_depth_nom):
                # always round result to next 0.5 mm
                tap_depth_nom = round(tap_depth_nom) + 0.5
            else:
                tap_depth_nom = round(tap_depth_nom)
            self.tapLengthLineEdit.setStyleSheet('background-color:white')
            return str(tap_depth_nom)
        except:
            pass

    def calculate_drill_depth(self, tap_depth, pitch):
        try:
            tap_depth = float(tap_depth)
            self.drillLengthLineEdit.setStyleSheet('background-color:white')
        except Exception as e:
            self.drillLengthLineEdit.setStyleSheet('background-color:red')
            return 'Lengthen Screw'
        try:
            pitch = float(pitch)
            tap_depth_max = tap_depth + 1
            bottom_tap_length = 2.5 * pitch + 1.5
            drill_depth_min = tap_depth_max + bottom_tap_length
            # defalut drill depth bilateral tolerance is 0.5mm
            drill_depth_nom = drill_depth_min + 0.5

            if drill_depth_nom > round(drill_depth_nom):
                # always round result to next 0.5 mm
                drill_depth_nom = round(drill_depth_nom) + 0.5
            else:
                drill_depth_nom = round(drill_depth_nom)
            return str(drill_depth_nom)
        except:
            print('Input a number')

    def update_clearance_hole(self):
        hole_diameter = self.clearanceHole(
            self.sizeCombo.currentText(), self.clearanceHoleCombo.currentText())
        self.clearanceHoleLineEdit.setText(hole_diameter)

    def clearanceHole(self, screwsize, type):
        screwsize = int(screwsize)
        try:
            self.conn = sqlite3.connect(
                self.resource_path('screwSelection.db'))
            cursor = self.conn.cursor()
            if type == 'Loose Fit':
                sql = "select loose_fit  from metric_profile where size =%s " % screwsize
                cursor.execute(sql)
                rs = cursor.fetchall()
            elif type == 'Middle Fit':
                sql = "select middle_fit  from metric_profile where size =%s" % screwsize
                cursor.execute(sql)
                rs = cursor.fetchall()
            elif type == 'Close Fit':
                sql = "select close_fit  from metric_profile where size =%s" % screwsize
                cursor.execute(sql)
                rs = cursor.fetchall()
            rs = [row[0] for row in rs]
            return str(rs[0])
        except Exception as e:
            print('Error here')
        finally:
            cursor.close()
            self.conn.close()

    def emit_sch(self):
        self.signal_clearance_hole.emit()

    def update_material(self):
        size = self.sizeCombo.currentText()
        self.outer_material_lineEdit.setText('Min. %s' % size)
        size = float(size)
        if size < 16:
            size = size / 2 + 8
        self.inner_material_lineEdit.setText('Min. %s' % str(size))
        self.bottom_material_lineEdit.setText('Min. 8')

    def display_join_thk(self):
        self.join_thk_display.setText(self.joinThicknessLineEdit.text())

    def display_screw_length(self):
        self.screw_length_display.setText(self.screwLengthcombo.currentText())

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS,
            # and places our data files in a folder relative to that temp
            # folder named as specified in the datas tuple in the spec file
            base_path = sys._MEIPASS
        except Exception:
            # sys._MEIPASS is not defined, so use the original path
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = boltSelection()

    sys.exit(app.exec_())
