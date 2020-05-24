import sys
import PyQt5
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt,QDir, QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,QFileDialog,QListWidget,QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
import quandl
import pandas as pd
import plotly
import plotly.graph_objects as go

#Mes fichiers
import excelImporter as ex
import dateUtils as date
import dataAnalysis as da

#Config
quandl.ApiConfig.api_key = "YOUR QUANDL API KEY"
Form, qtBaseClass = uic.loadUiType("dialog.ui")
sys.argv.append("--disable-web-security")

path = QDir.current().filePath('plotly-latest.min.js') 
local = QUrl.fromLocalFile(path).toString()
targetData = 'Open'

class Ui(QtWidgets.QDialog, Form):

    def displayFigureInBrowser(self,figure):         
        raw_html = '<html><head><meta charset="utf-8" />'
        raw_html += '<script src="{}"></script></head>'.format(local)        
        raw_html += '<body>'
        raw_html += plotly.offline.plot(figure, include_plotlyjs=False, output_type='div')
        raw_html += '</body></html>'
        self.browser.setHtml(raw_html)
        self.browser.show()  

    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)  

        #init
        company = ex.getCollumnInExcelFile("company.xlsx","Nom Euronext")
        company = ["EURONEXT/" + s for s in company]         
        self.listCompany.addItems(company)
        self.listCompany.itemClicked.connect(self.Clicked)

        #Bouton appliquer
        self.btnApply.clicked.connect(self.RefreshSettings)                
                
        #Bouton télécharger toutes les données
        self.btnDownloadAll.clicked.connect(self.DownloadAll)
        self.allQuandlDatas = pd.DataFrame()

        #Browser d'affichage des courbes
        self.browser  = QWebEngineView()   
        self.browserLay.addWidget(self.browser)               
    
    def DownloadAll(self):  
        itemsTextList =  [str(self.listCompany.item(i).text()) for i in range(self.listCompany.count())]        
        self.allQuandlDatas = quandl.get(itemsTextList,trim_start = self.dateEdit.text())
        print(self.allQuandlDatas) 

    def Clicked(self,item):    
        self.target = item.text()
        colName = self.cmbColName.currentText()

        if self.target + ' - ' + colName in self.allQuandlDatas:
            colName = self.target + ' - ' + colName
            print("found in dl data :" + colName)            
            data = self.allQuandlDatas[colName]
            open_ = self.allQuandlDatas[self.target + ' - Open']
            close_ = self.allQuandlDatas[self.target + ' - Last']
        else:
            print("get data " + self.target)
            dl = quandl.get(self.target,trim_start = self.dateEdit.text())
            data = dl[colName]   
            open_ = dl['Open']  
            close_ = dl['Last']     

        #init figure
        fig = go.Figure()
        #trace data
        fig.add_trace(go.Scatter( x=data.index.tolist(), y=data,name = self.target + ' - ' + colName))  
        
        pX,pY = da.determinePtsBelow(data, float(self.percentageValue.text()),float(self.absoluteDeltaPercentage.text()))
        #trace points
        fig.add_trace(go.Scatter( x=pX,y=pY, mode="markers", visible='legendonly',name="point en dessous %",textposition="bottom center"))      

        rsi = da.get_rsi( data )      
        # RSI with n = 14 ( so x + 14 )
        fig.add_trace(go.Scatter( x=data.index.tolist(), y=rsi,name="RSI"))

        self.displayFigureInBrowser(fig)

    def RefreshSettings(self):     
        if self.listCompany.currentItem() != None:     
            self.Clicked(self.listCompany.currentItem())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    # show window
    w.show() 
    sys.exit(app.exec_())