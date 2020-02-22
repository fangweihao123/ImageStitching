from ui import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui,Qt
from PyQt5.QtWidgets import QFileDialog,QLabel,QAbstractItemView, QTableWidget, QListWidget,QTableWidgetItem,QHBoxLayout

class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        # setting main window geometry
        desktop_geometry = QtWidgets.QApplication.desktop()  # 获取屏幕大小
        main_window_width = desktop_geometry.width()  # 屏幕的宽
        main_window_height = desktop_geometry.height()  # 屏幕的高
        rect = self.geometry()  # 获取窗口界面大小
        window_width = rect.width()  # 窗口界面的宽
        window_height = rect.height()  # 窗口界面的高
        x = (main_window_width - window_width) // 2  # 计算窗口左上角点横坐标
        y = (main_window_height - window_height) // 2  # 计算窗口左上角点纵坐标
        self.setGeometry(x, y, window_width, window_height)  # 设置窗口界面在屏幕上的位置
        #self.tableWidget.setGeometry(100,100,750,800)
        #self.tableWidget.resize(400, 600)
        layout = QHBoxLayout()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(4)
        self.tableWidget_2.setColumnCount(1)
        self.tableWidget_2.setRowCount(4)
        # 设置表格水平头标签
        self.tableWidget.horizontalHeader().setHidden(True)  # 隐藏行表头
        self.tableWidget.verticalHeader().setHidden(True)  #隐藏列表头
        # self.tableWidget.setHorizontalHeaderLabels(['图片1', '图片2'])
        # 设置不可编辑模式
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置图片的大小
        self.tableWidget.setIconSize(Qt.QSize(100 ,125))
        for i in range(5):  # 让列宽和图片相同
            self.tableWidget.setColumnWidth(i, 100)
        for i in range(4):  # 让行高和图片相同
            self.tableWidget.setRowHeight(i, 125)
        #self.tableWidget_2.setGeometry(, , 750, 800)
        self.tableWidget_2.horizontalHeader().setHidden(True)  # 隐藏行表头
        self.tableWidget_2.verticalHeader().setHidden(True)  # 隐藏列表头
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setIconSize(Qt.QSize(500, 130))
        for i in range(1):  # 让列宽和图片相同
            self.tableWidget_2.setColumnWidth(i, 500)
        for i in range(4):  # 让行高和图片相同
            self.tableWidget_2.setRowHeight(i, 130)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.tableWidget_2)
        self.setLayout(layout)
        # 无边框以及背景透明一般不会在主窗口中用到，一般使用在子窗口中，例如在子窗口中显示gif提示载入信息等等
        #self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        #self.setAttribute(Qt.WA_TranslucentBackground) # 背景透明
        self.re=[]
        self.imgName=[]
        #函数槽连接
        self.pushButton.clicked.connect(self.open_file)
        self.pushButton_2.clicked.connect(self.group)
        self.pushButton_3.clicked.connect(self.pano)


    def open_file(self):#打开文件选择图片
        #选择文件夹：
        #QFileDialog.getExistingDirectory(self, "选择文件夹", "/")
        #选择单个文件：
        #QFileDialog.getOpenFileName(self, "选择文件", "/", "All Files (*);;Text Files (*.txt)")
        #选择多个文件：
        #QtWidgets.QFileDialog.getOpenFileNames(self, "多文件选择", "/", "所有文件 (*);;文本文件 (*.txt)")
        #保存文件：
        #QtWidgets.QFileDialog.getSaveFileName(self, "文件保存", "/", "图片文件 (*.png);;(*.jpeg)")
        # self.img_dir = QFileDialog.getExistingDirectory(self)  # 选择文件夹名字
        # 返回选取内容的路径，多个目标用list存储
        self.imgName = QFileDialog.getOpenFileNames(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        if len(self.imgName[0])>20:
            print('there too many picture')
        else:
            for i in range(len(self.imgName[0])):
                k = int(i/5)
                g = i%5
                #实例化表格窗口条目
                # item = QTableWidgetItem()
                newItem = QTableWidgetItem(QtGui.QIcon(self.imgName[0][i]),'')
                #用户点击表格时，图片被选中
                # item.setFlags(Qt.ItemIsEnabled)
                #图片路径设置与图片加载
                # icon = QtGui.QIcon(imgName[0][i])
                # item.setIcon(QtGui.QIcon(icon))
                print(newItem,type(newItem),k,g)
                # 输出当前进行的条目序号
                # 将条目加载到相应行列中
                self.tableWidget.setItem(k,g,newItem)

    def group(self):
        from classifier import Classifier
        self.clear_tableWidget() # 清空tableWidget
        img_list = self.imgName[0]
        # c = Classifier('./image')
        c = Classifier(img_list)
        c.classify()
        self.re = c.getImageSet()
        self.update_tableWidget() # 更新tableWidget
        print(self.re)
        k = 0
        for each in self.re:
            len_each= len(each)
            for j in range(len_each):
                g = j%5
                #实例化表格窗口条目
                # item = QTableWidgetItem()
                #print(type(QtGui.QIcon(each[j])))
                newItem = QTableWidgetItem(QtGui.QIcon(each[j]),'')
                print(each[j],k,g)
                # 输出当前进行的条目序号
                # 将条目加载到相应行列中
                self.tableWidget.setItem(k,g,newItem)
            k = k+1

    def clear_tableWidget(self):
        self.tableWidget.clearContents()

    def update_tableWidget(self):
        print(len(self.re))
        le = 0
        for i in range(len(self.re)):
            if le<len(self.re[i]):
                le =len(self.re[i])
        print('le and each len:',le,len(self.re))
        self.tableWidget.setColumnCount(le)
        self.tableWidget.setRowCount(len(self.re))
        for i in range(le):  # 让列宽和图片相同
            self.tableWidget.setColumnWidth(i,int(551/le))
        for i in range(len(self.re)):  # 让行高和图片相同
            self.tableWidget.setRowHeight(i, int(531/len(self.re)))
        self.tableWidget.setIconSize(Qt.QSize(int(551/le), int(531/len(self.re)) ))

    def update_tableWidget_2(self):
        if len(self.re)<1:
            pass
        else:
            le = 1
            self.tableWidget_2.setColumnCount(le)
            self.tableWidget_2.setRowCount(len(self.re))
            for i in range(le):  # 让列宽和图片相同
                self.tableWidget_2.setColumnWidth(i,int(551/le))
            for i in range(len(self.re)):  # 让行高和图片相同
                self.tableWidget_2.setRowHeight(i, int(531/len(self.re)))
            self.tableWidget_2.setIconSize(Qt.QSize(int(551/le), int(531/len(self.re)) ))

    def pano(self):
        from pano import Stitch
        import cv2
        import os
        s = Stitch()
        self.update_tableWidget_2()
        cnt = 0
        if os.path.exists('../save'):
            print('already here')
        else:
            os.makedirs('../save')
            print("文件创建成功！")
        #print('re',self.re)
        for each in self.re:
            s.set_image_list(each)
            left = s.leftshift()
            right = s.rightshift()
            cv2.imwrite('../save/'+str(cnt) + '.jpg', right)
            cv2.waitKey(800)
            newItem = QTableWidgetItem(QtGui.QIcon('../save/'+str(cnt) + '.jpg'), '')
            # 将条目加载到相应行列中
            self.tableWidget_2.setItem(0, cnt, newItem)
            cnt = cnt + 1
            print('success!')

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv) #创建QApplication类的实例
    window = mywindow()
    window.show()#显示程序主窗口
    sys.exit(app.exec_())#开启事件主循环
