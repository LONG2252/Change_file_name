import os
import sys
from datetime import datetime
from update_file_name_ui import Ui_MainWindow
from PyQt6.QtWidgets import  (
    QApplication,QMainWindow,QMessageBox
)
from tkinter import (
    filedialog,Tk
)

config_file_path=r'config.ini'
log_path=r'log.txt'


class MainWindow(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.path=''
        self.get_config()
        self.out_textBrowser.setText('开始运行！')
        self.file_count=0
        self.button_start.clicked.connect(self.work_start)
        self.button_set_file_path.clicked.connect(self.set_path)
        self.the_old_scar=self.old_scar.text()
        self.the_new_scar=self.new_scan.text()


    def get_config(self):#获取配置文件
        try:
            with open(config_file_path, "r+", encoding='utf-8') as f:
                data=f.read().split('\n')
                for row in data:
                    if(row[:9]=='last_path' and len(row)> 11):
                        self.path=row[10:]
                        self.file_path.setText(self.path)
                f.close()
        except Exception as e:
            message = '获取配置文件报错： ' + str(e)
            self.add_log(message)
    def add_log(self,log): #方法：写入日志
        nowtime=datetime.now()
        log=str(nowtime) + ' - ' + log
        try:
            with open(log_path,'a',encoding='utf-8') as f:
                f.write(log)
                f.close()
        except Exception as  e:
            message='写入日志报错：' + str(e)
            self.QMBox(message)
    def add_config(self):#写入配置文件
        try:
            with open(config_file_path,'a+',encoding='utf-8') as f:
                if(self.path != None):
                    data='last_path' + ':' + self.path
                    f.write(data)
                    f.write('\n')
                f.close()
        except Exception as e:
            message = '写入配置文件出错： ' + str(e)
            self.add_log(message)

    def chack_add_path(self):
        try:
            if (os.path.isdir(self.file_path.text())):
                self.path = self.file_path.text()
                return 1
            else:
                if (os.path.isdir(self.path)):
                    return 1
                else:
                    return 0
        except Exception as e:
            print(e)
            return 0

    def work_start(self):#工作开始
        self.new_scar_str = self.new_scan.text()
        self.old_scar_str = self.old_scar.text()
        start_time=datetime.now()#开始时间
        s=0
        if(self.chack_add_path()):
            if (self.choice_add.isChecked()):  # 添加前缀
                if (self.new_scar_str != None):
                    filelist=self.scan_file(self.path)
                    for row in filelist:
                        if(os.path.isfile(row)):
                            self.add_name(row,self.new_scar_str)
                    s=1

            elif (self.choice_delete.isChecked()):  # 删除前缀
                if (self.old_scar_str != None):
                    filelist=self.scan_file(self.path)
                    for row in filelist:
                        if(os.path.isfile(row)):
                            self.update_name(row,self.old_scar_str,'')
                    s = 1
            elif (self.choice_update.isChecked()):  # 替换前缀
                if (self.old_scar_str != None and self.new_scar_str != None ):
                    filelist = self.scan_file(self.path)
                    for row in filelist:
                        if (os.path.isfile(row)):
                            self.update_name(row, self.old_scar_str,self.new_scar_str)
                    s = 1
                else:
                    message = '新前缀或旧前缀为空'
                    self.QMBox(message)
            else:
                message = '请选择要使用的功能，更新，删除，替换！'
                self.QMBox(message)
            if(s==1):
                self.add_config()
                end_time = datetime.now()
                message = '\n程序执行完成，开始于：' + str(start_time) + ', 结束于：' + str(end_time) + ',总共修改成功文件数：' + str(self.file_count) + '\n'
                self.file_count = 0
                self.out_textBrowser.append(message)
                QApplication.processEvents()

        else:
            message='请设置文件夹路径！'
            self.QMBox(message)

    def add_name(self,file,scar):#添加前缀
        file_path = os.path.dirname(file)
        file_name = os.path.basename(file)
        scar_leng = len(scar)
        if (scar != file_name[:scar_leng]):
            new_file = file_path + '/' + scar + file_name
            try:
                os.rename(file, new_file)
                message='文件： ' + new_file +' 更新成功！'
                self.out_textBrowser.append(message)
                QApplication.processEvents()
                self.file_count=self.file_count+1
            except Exception as e:
                message='修改文件名: ' + file +'报错： ' + str(e)
                self.QMBox(message)
        else:
            message = '文件： ' + file + '已经有了同样的前缀！   ' + file_name[:scar_leng]
            self.out_textBrowser.append(message)
            QApplication.processEvents()
    def update_name(self,file,old_scar,new_scar):#更新前缀(包含删除跟替换，如果删除，只需要将新前缀设置为‘’即可，)
        file_path = os.path.dirname(file)
        file_name = os.path.basename(file)
        #new_scar_leng = len(new_scar)
        old_scar_len = len(old_scar)
        if (old_scar == file_name[:old_scar_len] and len(old_scar) !=0 ):#匹配旧字符串
            new_file = file_path + '/' + new_scar + file_name[old_scar_len:]
            try:
                os.rename(file, new_file)
                message = '文件： ' + new_file + ' 更新成功！'
                self.out_textBrowser.append(message)
                QApplication.processEvents()
                self.file_count = self.file_count + 1
            except Exception as e:
                message='修改文件名: ' + file +'报错： ' + str(e)
                self.QMBox(message)
        else:
            message = '文件： ' + file + '不包含同样的前缀！   ' + old_scar
            self.out_textBrowser.append(message)
            QApplication.processEvents()

    def scan_file(self,path,file_list=[]):
        self.out_textBrowser.append('开始扫描文件！')
        QApplication.processEvents()
        if (os.path.exists(path)):
            files = os.listdir(path)
            for row in files:
                if (row[1:5] == 'RECY' or row[1:5] == 'yste'):
                    files.remove(row)
            for file in files:
                if (os.path.isdir(os.path.join(path, file))):
                    self.scan_file(os.path.join(path, file), file_list)
                else:
                    file = os.path.join(path, file)
                    file_list.append(file)

            return file_list
    def set_path(self):
        self.path = self.get_directory()

        if(self.path != 0):
            self.file_path.setText(self.path)
        else:
            message = '请重新设置文件夹路径！ '
            self.QMBox(message)
    def get_directory(self): #调用本地资源管理器选择本地文件
        try:
            root = Tk()
            root.withdraw()
            #file_path = filedialog.askopenfilename()#调用本地资源管理器，获取本地文件的绝对路径
            file_path=filedialog.askdirectory()#调用本地资源管理器，获取文件夹的绝对路径
            if(file_path != None and os.path.isdir(file_path)):
                return file_path
            else:
                message =file_path +  '  不是文件夹！'
                self.QMBox(message)
                return 0
        except Exception as e:
            message='打开文件失败： ' + str(e)
            self.QMBox(message)

    def QMBox(self, message):  # 弹窗方法 选则是，返回1，选择否，返回0
        reply = QMessageBox.question(self, '信息提示', message)
        if (str(reply) == 'StandardButton.Yes'):
            return 1
        else:
            return 0

if __name__=="__main__":

    app = QApplication(sys.argv)
    mywindow = MainWindow()
    sys.exit(app.exec())