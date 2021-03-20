import sys
from PyQt5 import (
    QtCore,
    QtWidgets
    )
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QToolTip,
    QInputDialog,
    QLineEdit,
    QFileDialog
    )

# enable high dpi scaling for 4k screens
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("Test Application - Find Errors")
        self.setGeometry(200, 200, 550, 300) # first two numbers: location on screen, last two numbers: Height and Width
        self.initUI()
        self.textBrowser_path.append(f'Please choose a file')
        
    def initUI(self):
        # generate label
        self.pathLabel = QtWidgets.QLabel(self)
        self.pathLabel.setText("Path from file:")
        self.pathLabel.adjustSize()
        self.pathLabel.move(20, 5)

        # generate button 1 and connect with function
        self.button_chooseFile = QPushButton('Browse', self)
        self.button_chooseFile.setGeometry(QtCore.QRect(450, 10, 75, 23))
        self.button_chooseFile.clicked.connect(self.openFileNameDialog)

        # generate button 2 and connect with function
        self.button_submit = QPushButton('Submit', self)
        self.button_submit.setGeometry(QtCore.QRect(450, 42, 75, 23))
        self.button_submit.clicked.connect(self.submitClicked)

        # generate text browser to show path of selected file
        self.textBrowser_path = QtWidgets.QTextEdit(self)
        self.textBrowser_path.setGeometry(QtCore.QRect(20, 25, 420, 40))
        self.textBrowser_path.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textBrowser_path.setObjectName("textBrowser_path")

        # generate text browser to show output
        self.textBrowser_result = QtWidgets.QTextBrowser(self)
        self.textBrowser_result.setGeometry(QtCore.QRect(20, 90, 508, 200))
        self.textBrowser_result.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textBrowser_result.setObjectName("textBrowser_result")

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.path, _ = QFileDialog.getOpenFileName(self,"Test Application - Find Errors", "","All Files (*);;Python Files (*.py)", options=options)
        if self.path:
            self.textBrowser_path.clear()
            self.textBrowser_path.append(f'{self.path}')

    def submitClicked(self):
        self.textBrowser_result.clear()             # clear textbrowser from displayed output
        count_line = 0
        count_overall = 1
        keywords = (                                # specify here what you are looking for. @todo: make it parameterizable
            'error99',
            'test',
            'words'
        )
        errorCodes = {                              # specifie here all errorcodes. @todo destinguish betwenn products
            1: (62, 'Z-axis general'),
            2: (63, 'Z-axis high voltage'),
            3: (64, 'X-axis')
            }
        result = dict()
        
        try:
            for keyword in keywords:
                file = open(self.path, "r")                     # do this for each specified error
                for line in file:                               # check every line in file
                    count_line += 1                             # increment counter 
                    if keyword in line:                         # check if specified error is in line and if it is:
                        result[count_overall] = {'keyword' : keyword, 'line' : str(count_line), 'text' : line}   # create new entry in dictionary with all its informations
                        count_overall += 1                      # increment counter
                count_line = 0                                  # reset counter

            if len(result) > 0:
                for num in result:                                  # extract information from dictionary and display it in textbrowser                 
                    self.textBrowser_result.append(
                        f'Number {num}  -  \
                        Keyword: {result[num]["keyword"]}  -  \
                        Line in file: {result[num]["line"]}'
                        )
                    self.textBrowser_result.append(f'{result[num]["text"]}')
                    for i in range(1, len(errorCodes) + 1):
                        if str(errorCodes.get(i)[0]) in result[num]["text"]:
                            self.textBrowser_result.append(f'--> Error meaning: {errorCodes.get(i)[1]}')
                            self.textBrowser_result.append(f'--------------------------------------------------------------------------------------------------------\n')
            else:
                self.textBrowser_result.append(f'No errors found')
            
            file.close()
                    
        except:
            self.textBrowser_path.clear()
            self.textBrowser_path.append(f'No valid file or an error occured - Please choose a file')

def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':    
    main()
