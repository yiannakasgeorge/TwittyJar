import sys
import tweetsUI
import worker
import models
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog

class MainDialog(QDialog, tweetsUI.Ui_Dialog):
   
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)

        self.cancelBtn.setEnabled(False)
        self.searchBtn.clicked.connect(self.search)
        self.cancelBtn.clicked.connect(self.cancel)

        self.input_fromthisdate.setDate(QDate().currentDate().addDays(-1))
        self.input_tothisdate.setDate(QDate().currentDate()) 
        
        self.checkBox_useProxy.stateChanged.connect(self.toggleProxyInputState)

        self.workerClient = worker.Client(None,self)

    @staticmethod
    def getFormValues(form):
        
        formSeachCriteria = models.FormSeachCriteria()
        formSeachCriteria.setAllOfTheseWords(form.input_allofthesewords.text())    
        formSeachCriteria.setThisExactPhrase(form.input_thisexactphrase.text())    
        formSeachCriteria.setAnyOfTheseWords(form.input_anyofthesewords.text())    
        formSeachCriteria.setNoneOfTheseWords(form.input_noneofthesewords.text())    
        formSeachCriteria.setTheseHashtags(form.input_thesehashtags.text())   
        formSeachCriteria.setLanguage(models.Languages.getLanguageValue(form.input_writtenin.currentIndex()))    
        formSeachCriteria.setFromTheseAccounts(form.input_fromtheseaccounts.text())    
        formSeachCriteria.setToTheseAccounts(form.input_totheseaccounts.text())    
        formSeachCriteria.setMentioningTheseAccounts(form.input_mentioningtheseaccounts.text())    
        formSeachCriteria.setNearThisPlace(form.input_nearthisplace.text())    
        formSeachCriteria.setFromThisDate(form.input_fromthisdate.text())    
        formSeachCriteria.setToThisDate(form.input_tothisdate.text())  
        formSearchCriteriaValid = formSeachCriteria.isValidForm()
        
        formExportOptions = models.FormExportOptions()
        formExportOptions.setExportFilename(form.input_filename.text())
        formExportOptions.setExportPermalink(form.checkBox_getPermalink.isChecked())
        formExportOptions.setExportTweetID(form.checkBox_getTweetID.isChecked())
        formExportOptions.setExportPosterUsername(form.checkBox_getTweetPostersUsername.isChecked())
        formExportOptions.setExportTweetDate(form.checkBox_getTweetDate.isChecked())
        formExportOptions.setExportPosterProfileName(form.checkBox_getTweetPostersProfileName.isChecked())
        formExportOptions.setExportTweetText(form.checkBox_getTweetText.isChecked())
        formExportOptions.setExportNumOfRetweets(form.checkBox_getTweetsNumberOfRetweets.isChecked())
        formExportOptions.setExportRetweetStatus(form.checkBox_getTweetRetweetStatus.isChecked())
        formExportOptions.setExportFollowersCount(form.checkBox_getFollowersCount.isChecked())
        formExportOptionsValid = True

        formProxyOptions = models.FormProxyOptions()
        formProxyOptions.setUseProxy(form.checkBox_useProxy.isChecked())
        formProxyOptions.setProxyURL(form.input_proxyUrl.text())
        if formProxyOptions.useProxy and formSearchCriteriaValid == False:
            formProxyOptionsValid = True
        else:
            formProxyOptionsValid = formProxyOptions.isValidProxyOptions()
    

        formOptions = models.FormOptions()
        formOptions.setFormExportOptions(formExportOptions)
        formOptions.setFormProxyOptions(formProxyOptions)
        formOptions.setFormSearchCriteria(formSeachCriteria)

        if(formSearchCriteriaValid and formExportOptionsValid and formProxyOptionsValid):
            return {"valid": True, "formData": formOptions}
        else:
            return {"valid": False, "formStatus": {"formSearchCriteriaValid": formSearchCriteriaValid, "formExportOptionsValid": formExportOptionsValid, "formProxyOptionsValid": formProxyOptionsValid}}

    @pyqtSlot()
    def search(self):
        self.workerClient.toggle(True)   
        
    @pyqtSlot()
    def cancel(self):
        self.workerClient.toggle(False)     

    @pyqtSlot()
    def toggleProxyInputState(self):
        if self.checkBox_useProxy.isChecked():
            self.input_proxyUrl.setEnabled(True)
        else:
            self.input_proxyUrl.setEnabled(False)
   
       
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    application = MainDialog()
    application.show()
    sys.exit(app.exec_())



