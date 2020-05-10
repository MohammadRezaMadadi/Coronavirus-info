# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'corona.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import time
from random import random


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(933, 592)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.UpdateButton = QtWidgets.QPushButton(self.centralwidget)
        self.UpdateButton.setEnabled(True)
        self.UpdateButton.setGeometry(QtCore.QRect(736, 528, 93, 40))
        self.UpdateButton.setMouseTracking(False)
        self.UpdateButton.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.UpdateButton.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.UpdateButton.setObjectName("UpdateButton")
        self.ExitButton = QtWidgets.QPushButton(self.centralwidget)
        self.ExitButton.setGeometry(QtCore.QRect(829, 528, 97, 40))
        self.ExitButton.setObjectName("ExitButton")
        self.massbox = QtWidgets.QTextBrowser(self.centralwidget)
        self.massbox.setGeometry(QtCore.QRect(260, 503, 471, 66))
        self.massbox.setObjectName("massbox")
        self.countrybox = QtWidgets.QTextBrowser(self.centralwidget)
        self.countrybox.setGeometry(QtCore.QRect(2, 2, 256, 567))
        self.countrybox.setObjectName("countrybox")
        self.graph = QtWidgets.QLabel(self.centralwidget)
        self.graph.setGeometry(QtCore.QRect(261, 4, 668, 496))
        self.graph.setPixmap(QtGui.QPixmap(""))
        self.graph.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.graph.setObjectName("graph")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.UpdateButton.clicked.connect(self.UpdateData)
        self.ExitButton.clicked.connect(self.CloseApp)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Corona Project..."))
        self.UpdateButton.setText(_translate("MainWindow", "Update"))
        self.ExitButton.setText(_translate("MainWindow", "Exit"))
        self.graph.setText(_translate("MainWindow", "\n"
                                      "The first fifteen countries"))

    def UpdateData(self):
        self.massbox.append('Starting...')
        app.processEvents()
        with open('countery_text.txt','w')as file:
            response = requests.get('https://www.worldometers.info/coronavirus/')
            web_site = response.text 
            soup = BeautifulSoup(web_site,'html.parser')
            table_list = soup.find_all('table', attrs={'id':'main_table_countries_today'})
            table = table_list[0]
            
        #Read head of row
            thead_list = table.find('thead')
            th_tr_list = thead_list.find_all('tr')
            th_tr = th_tr_list[0]
            th_list = th_tr.find_all('th')
            th_list_text = []
            for this_th in th_list:
                this_list_text1 = this_th.text
                th_list_text += [
                    this_list_text1
                    ]
            self.countrybox.append('List of country and total case:')
            self.countrybox.append('-----------------------------------')

            for th_item in th_list_text:
                file.write(th_item +' |')
            file.write('\n')
            
        # Read each country
            tbody = table.find('tbody')
            tr_list = tbody.find_all('tr')

            for tr_len in range(len(tr_list)):
                tr = tr_list[tr_len]
                td_list = tr.find_all('td')
                td_list_text = []

                for this_td in td_list:
                    this_list_text = this_td.text
                    if this_list_text == ' ' or this_list_text == '':
                        this_list_text = 'Null'
                    
                    td_list_text += [
                        this_list_text
                    ]
                    
        #  write in the file
                for td_item in td_list_text:
                    file.write(td_item + ' |')
                file.write('\n')
        self.massbox.append(f"{len(tr_list)} countries found...")
        time.sleep(random() * 5 )
        self.massbox.append('writing in the text file...')
        time.sleep(random() * 10 )
        self.massbox.append("Please wait, program's making the Graph...")

        with open("countery_text.txt", 'r') as infile:
            file_data = infile.readlines()

            countries = []
            values = []
            countri = []
            valu = []
            for line_number in range(25,len(file_data)):
                convt1 = ''
                this_line_str = file_data[line_number]
                this_line_list = this_line_str.split(' |')
                country = this_line_list[0]

                if this_line_list[1]=='Null':
                    continue
                else:
                    total_case = (this_line_list[1])
                    for i in total_case:
                        if i == ',':
                            continue
                        else:
                            convt1 += i

                    valu.append(int(convt1))
                    countri.append(country)
                    self.countrybox.append(country+': '+convt1)

            for line_number in range(25,40):
                convt = ''
                this_line_str = file_data[line_number]
                this_line_list = this_line_str.split(' |')
                country = this_line_list[0]

                if this_line_list[1]=='Null':
                    continue
                else:
                    total_case = (this_line_list[1])
                    for i in total_case:
                        if i == ',':
                            continue
                        else:
                            convt += i

                    values.append(int(convt))
                    countries.append(country)

            plt.figure(figsize=(10, 7))
            plt.subplot(111)
            plt.bar(countries, values)
            plt.savefig('CoGraph.svg', format='svg')
            self.graph.setPixmap(QtGui.QPixmap("CoGraph.svg"))

    def CloseApp(self):
        sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
