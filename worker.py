import codecs
import sys
import main 
import os
from searchController import * 
from functools import partial
from PyQt5 import QtCore
from PyQt5.QtCore import  QMutex, QObject, QThread, pyqtSignal, pyqtSlot

class Worker(QtCore.QThread):
    
    sgnOutput = pyqtSignal(str)
    sgnFinished = pyqtSignal()
 
    def __init__(self, parent=None, *args, **kwargs):
        QtCore.QThread.__init__(self, parent)
        self.setFormOptions(*args, **kwargs)
        self._mutex = QMutex()
        self._running = True

    def setFormOptions(self, form):
        self.form = form
        self.formOptions = form.formOptions
        self.formSearchCriteria = self.formOptions.formSearchCriteria
        self.formExportOptions = self.formOptions.formExportOptions
        self.formProxyOptions = self.formOptions.formProxyOptions
        return False

    def on_message_output(self, message):
        self.outputTxtInput = message

    @pyqtSlot()
    def stop(self):
        self._mutex.lock()
        self._running = False
        self._mutex.unlock()

    def running(self):
        try:
            self._mutex.lock()
            return self._running
        finally:
            self._mutex.unlock()

    @pyqtSlot()
    def run(self):
        
        formSearchCriteria = self.formSearchCriteria
        fileName = self.formExportOptions.filename
        columnsHeading = ''
        columnNumber = 0 
        placeholders = '\n'
        fieldsColumnsMap = models.FormExportOptions.getMappingsBetweenExportFieldsAndColumnNames()

        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        filePath = os.path.join(desktop, fileName)

        for attr,value in vars(self.formExportOptions).items():

            if(value != False and attr != 'filename'):
                if(columnNumber != 0):
                    placeholders += '\t' #tab delimiter
                    columnsHeading += '\t' #tab delimiter

                columnsHeading += fieldsColumnsMap[attr]
                placeholders += "{0." + attr +"}"
                columnNumber += 1

        try:
           
            outputFile = codecs.open(filePath, "w+", "utf_8_sig")
            outputFile.write(columnsHeading)
            tweetsIds = []
        
            def receiveBuffer(tweets):
                for t in tweets:
                    if t.id not in tweetsIds:
                        # print(t.__dict__)
                        outputFile.write(placeholders.format(t))
                        tweetsIds.append(t.id)
                        outputFile.flush()
                        self.sgnOutput.emit('%d tweets saved ... ' % len(tweetsIds) + '\nTweet retrieved date and time: ' + t.dateTime + '\n')
                            
                    
            self.sgnOutput.emit('Searching...\n')
            SearchController.getTweets(self, receiveBuffer) 

        except Exception as ex:
            outputFile.close()
            self.sgnFinished.emit()
            self.sgnOutput.emit("An error occured. Please try again. Error: " + str(ex))
           

        finally:
            outputFile.close()
            self.sgnFinished.emit()
            if(len(tweetsIds) == 0):
                self.sgnOutput.emit('No results found! Try another search.')
            else:
                self.sgnOutput.emit('Results saved in:  "%s".' % fileName)
            
                   
class Client(QObject):

    sgnOutput = pyqtSignal(str)

    def __init__(self, parent=None, *args, **kwargs):
        QObject.__init__(self, parent)
        self.setFormData(*args, **kwargs)
        self._thread = None
        self._worker = None

    def setFormData(self, form):
        self.form = form
        self.outputField = form.outputTxtInput

    @pyqtSlot()
    def onOutputMessage(self, info):
        self.outputField.append(str(info))


    def toggle(self, enable, *args, **kwargs):
        
        if enable:
            if not self._thread:
                self._thread = QThread()
            
            formOptions = main.MainDialog.getFormValues(self.form)
            self.form.outputTxtInput.clear()
            
            if formOptions['valid'] == False:
                errorMsg = 'Errors:\n\n'
                if formOptions['formStatus']['formSearchCriteriaValid'] == False:
                    errorMsg += 'Fill at least one search criteria.\n'
                if formOptions['formStatus']['formExportOptionsValid'] == False:
                    errorMsg += 'Use a valid export filename and select at least one export option.\n'
                if formOptions['formStatus']['formProxyOptionsValid'] == False:
                    errorMsg += 'Use a valid Proxy URL - Unable to connect.\n'
                self.form.outputTxtInput.append(errorMsg)
                return

            self.form.formOptions = formOptions['formData']
            self.form.searchBtn.setEnabled(False)
            self.form.cancelBtn.setEnabled(True)
            self._worker = Worker(None, self.form)
            self.sgnOutput.connect(self._worker.on_message_output)
            self._worker.moveToThread(self._thread)
            self._worker.sgnOutput.connect(partial(self.onOutputMessage))
            self._worker.sgnFinished.connect(partial(self.on_worker_done))
           
            
            self._thread.started.connect(self._worker.run)
            self._thread.start()
          
        else:
           
            self._worker.sgnOutput.emit('Cancelling search, please wait ...')
            self._worker.stop()
            self.on_worker_done(True)

    @pyqtSlot()
    def on_worker_done(self, userInterruption=False):
        self.form.searchBtn.setEnabled(True)
        self.form.cancelBtn.setEnabled(False)
        self._thread.quit()
        self._thread.wait()
       
       