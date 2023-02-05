import sys
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from ui_Login import Ui_LoginWindow
from ui_splash_screen import Ui_SplashScreen
from ui_Dashboard import Ui_DashBoardWindow

counter = 0


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main = LoginWindow()
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # REMOVE TITLE BAR
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        # START QTIMER
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IS IN MILLISECONDS
        self.timer.start(35)
        # initial description
        self.ui.label_description.setText("<strong>WELCOME</strong> TO OUR BANK")
        self.ui.label_loading.setText("<style>color: rgb(98, 114, 164);</style>loading.")
        # changing text
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong>"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>FETCHING DATA</strong>"))

        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_loading.setText("<style>color: rgb(98, 114, "
                                                                             "164);</style>loading.."))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_loading.setText("<style>color: rgb(98, 114, "
                                                                             "164);</style>loading..."))
        self.show()

    def progress(self):
        global counter
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH AND OPEN APP
        if counter > 100:
            self.timer.stop()
            counter = 0
            self.main.show()
            self.close()

        counter += 1


# returns password
def return_password(number: str):
    file = open("./data/" + number, "r")
    password = (file.readlines()[2]).strip('\n')
    file.close()
    return password


# returns first name
def return_first_name(number: str):
    file = open("./data/" + number, "r")
    name = (file.readlines()[0]).strip('\n')
    file.close()
    return name


# returns first name
def return_last_name(number: str):
    file = open("./data/" + number, "r")
    name = (file.readlines()[1]).strip('\n')
    file.close()
    return name


def return_current_amount(number: str):
    file = open("./data/" + number, "r")
    amount = (file.readlines()[6]).strip('\n')
    file.close()
    return amount


def deposit(number: str, amount: str):
    current_amount = return_current_amount(number)
    new_amount = int(current_amount) + int(amount)

    file_read = open("./data/" + number, "r")
    lines = file_read.readlines()
    file_read.close()
    lines[6] = str(new_amount)

    file_write = open("./data/" + number, "w")

    for index in range(len(lines)):
        file_write.writelines(lines[index])
    file_write.close()


def withdraw(number: str, amount: str):
    current_amount = return_current_amount(number)
    new_amount = int(current_amount) - int(amount)

    file_read = open("./data/" + number, "r")
    lines = file_read.readlines()
    file_read.close()
    lines[6] = str(new_amount)

    file_write = open("./data/" + number, "w")

    for index in range(len(lines)):
        file_write.writelines(lines[index])
    file_write.close()


def send_money(sender, receiver, amount):
    withdraw(sender, amount)
    deposit(receiver, amount)


class User:
    account_number: str = 'none'


class LoginWindow(QMainWindow):
    # create int for checking window status the default is normal
    win_status: int = 0

    def return_account_number(self):
        return self.ui.accountNumberLineEdit.text()

    def minimize_app(self):
        self.showMinimized()

    def restore_or_maximize_app(self):
        if self.win_status == 0:
            self.showMaximized()
            self.win_status = 1
        else:
            self.showNormal()
            self.win_status = 0

    def signin(self):
        if self.ui.accountNumberLineEdit.text() == "":
            self.ui.errorSigninLabel.clear()
            self.ui.errorSigninLabel.setText("Please enter account number")
        elif self.ui.passwordSigninLineEdit.text() == "":
            self.ui.errorSigninLabel.clear()
            self.ui.errorSigninLabel.setText("Please enter password")
        elif os.path.exists("./data/" + self.ui.accountNumberLineEdit.text()) == 0:
            self.ui.errorSigninLabel.clear()
            self.ui.errorSigninLabel.setText("Account does not exist")
        elif return_password(self.ui.accountNumberLineEdit.text()) != self.ui.passwordSigninLineEdit.text():
            self.ui.errorSigninLabel.setText("Incorrect Password")
        else:
            self.ui.errorSigninLabel.clear()
            User.account_number = self.ui.accountNumberLineEdit.text()
            self.close()
            self.dashboard = Dashboard()
            self.dashboard.show()

    def create_account(self, first_name, last_name, password, gender, sub_city, birthdate):
        data = [str(first_name), str(last_name), str(password), str(gender), str(sub_city), str(birthdate), "0"]

        if self.ui.firstNameLineEdit.text() == "":
            self.ui.errorCreateAccountLabel.clear()
            self.ui.errorCreateAccountLabel.setText("Please enter First Name")
        elif self.ui.lastNameLineEdit.text() == "":
            self.ui.errorCreateAccountLabel.clear()
            self.ui.errorCreateAccountLabel.setText("Please enter Last Name")
        elif self.ui.passwordCreateAccountLineEdit.text() == "":
            self.ui.errorCreateAccountLabel.clear()
            self.ui.errorCreateAccountLabel.setText("Please enter Password")
        else:
            for acc_num in range(10000, 100000000000):
                if os.path.exists("./data/" + str(acc_num)):
                    acc_num += 1
                else:
                    file = open("./data/" + str(acc_num), "w")
                    # Set the user's account number for it to be passed to the other window through the class "User"
                    User.account_number = str(acc_num)

                    for index in range(len(data)):
                        file.writelines(data[index])
                        file.writelines("\n")
                    file.close()
                    break
            self.close()
            # error below here
            self.dashboard = Dashboard()
            self.dashboard.show()

    def __init__(self):
        QMainWindow.__init__(self)

        self.dashboard = None
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        # make default buttons disappear
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # give function to close button
        close_button = self.ui.closeApp
        close_button.clicked.connect(lambda: self.close())

        # make minimize button
        minimize_button = self.ui.minimizeApp
        minimize_button.clicked.connect(self.minimize_app)

        # make maximize or restore
        self.ui.maximiseApp.clicked.connect(self.restore_or_maximize_app)

        # function for create account and back button
        self.ui.createAccountButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.backCreateAccountButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))

        # function for signin button
        self.ui.doneSigninButton.clicked.connect(lambda: self.signin())

        # change look of the password line edit
        self.ui.passwordSigninLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.passwordCreateAccountLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        # give function to create account button
        self.ui.doneCreateAccountButton.clicked.connect(
            lambda: self.create_account(str.upper(self.ui.firstNameLineEdit.text()),
                                        str.upper(self.ui.lastNameLineEdit.text()),
                                        self.ui.passwordCreateAccountLineEdit.text(),
                                        self.ui.genderComboBox.currentText(),
                                        self.ui.subCityComboBox.currentText(),
                                        str(self.ui.birthDateDateComboBox.currentText())
                                        + " "
                                        + str(self.ui.birthDateMonthComboBox.currentText())
                                        + " "
                                        + str(self.ui.birthDateYearSpinBox.text())))


class Dashboard(QMainWindow):
    # win_status = 0 means that it is on a normal state
    win_status = 0

    def my_account_button(self):
        self.ui.myAccountButton.setStyleSheet("background-color: rgb(76, 79, 121);")

        self.ui.sendMoneyButton.setStyleSheet("")
        self.ui.depositButton.setStyleSheet("")
        self.ui.withdrawButton.setStyleSheet("")
        self.ui.aboutButton.setStyleSheet("")

        # clear the line edits and spin Boxes
        self.ui.sendMoneyAccountNumberLineEdit.clear()
        self.ui.sendMoneyAmountSpinBox.setValue(1)
        self.ui.sendMoneyConfirmPasswordLineEdit.clear()
        self.ui.depositAmountSpinBox.setValue(1)
        self.ui.depositConfirmPasswordLineEdit.clear()
        self.ui.withdrawAmountSpinBox.setValue(1)
        self.ui.withdrawConfirmPasswordLineEdit.clear()

        # change current index for the stacked widget
        self.ui.stackedWidget.setCurrentIndex(0)

    def send_money_button(self):
        self.ui.sendMoneyButton.setStyleSheet("background-color: rgb(76, 79, 121);")

        self.ui.myAccountButton.setStyleSheet("")
        self.ui.depositButton.setStyleSheet("")
        self.ui.withdrawButton.setStyleSheet("")
        self.ui.aboutButton.setStyleSheet("")

        # clear the line edits and spin Boxes
        self.ui.sendMoneyAccountNumberLineEdit.clear()
        self.ui.sendMoneyAmountSpinBox.setValue(1)
        self.ui.sendMoneyConfirmPasswordLineEdit.clear()
        self.ui.depositAmountSpinBox.setValue(1)
        self.ui.depositConfirmPasswordLineEdit.clear()
        self.ui.withdrawAmountSpinBox.setValue(1)
        self.ui.withdrawConfirmPasswordLineEdit.clear()

        self.ui.errorSendMoneyLabel.clear()
        self.ui.errorDepositLabel.clear()
        self.ui.errorWithdrawLabel.clear()

        self.ui.stackedWidget.setCurrentIndex(1)

    def deposit_button(self):
        self.ui.depositButton.setStyleSheet("background-color: rgb(76, 79, 121);")

        self.ui.sendMoneyButton.setStyleSheet("")
        self.ui.myAccountButton.setStyleSheet("")
        self.ui.withdrawButton.setStyleSheet("")
        self.ui.aboutButton.setStyleSheet("")

        # clear the line edits and spin Boxes
        self.ui.sendMoneyAccountNumberLineEdit.clear()
        self.ui.sendMoneyAmountSpinBox.setValue(1)
        self.ui.sendMoneyConfirmPasswordLineEdit.clear()
        self.ui.depositAmountSpinBox.setValue(1)
        self.ui.depositConfirmPasswordLineEdit.clear()
        self.ui.withdrawAmountSpinBox.setValue(1)
        self.ui.withdrawConfirmPasswordLineEdit.clear()

        self.ui.errorSendMoneyLabel.clear()
        self.ui.errorDepositLabel.clear()
        self.ui.errorWithdrawLabel.clear()

        self.ui.stackedWidget.setCurrentIndex(2)

    def withdraw_button(self):
        self.ui.withdrawButton.setStyleSheet("background-color: rgb(76, 79, 121);")

        self.ui.sendMoneyButton.setStyleSheet("")
        self.ui.depositButton.setStyleSheet("")
        self.ui.myAccountButton.setStyleSheet("")
        self.ui.aboutButton.setStyleSheet("")

        # clear the line edits and spin Boxes
        self.ui.sendMoneyAccountNumberLineEdit.clear()
        self.ui.sendMoneyAmountSpinBox.setValue(1)
        self.ui.sendMoneyConfirmPasswordLineEdit.clear()
        self.ui.depositAmountSpinBox.setValue(1)
        self.ui.depositConfirmPasswordLineEdit.clear()
        self.ui.withdrawAmountSpinBox.setValue(1)
        self.ui.withdrawConfirmPasswordLineEdit.clear()

        self.ui.errorSendMoneyLabel.clear()
        self.ui.errorDepositLabel.clear()
        self.ui.errorWithdrawLabel.clear()

        self.ui.stackedWidget.setCurrentIndex(3)

    def about_button(self):
        self.ui.aboutButton.setStyleSheet("background-color: rgb(76, 79, 121);")

        self.ui.sendMoneyButton.setStyleSheet("")
        self.ui.depositButton.setStyleSheet("")
        self.ui.withdrawButton.setStyleSheet("")
        self.ui.myAccountButton.setStyleSheet("")

        # clear the line edits and spin Boxes
        self.ui.sendMoneyAccountNumberLineEdit.clear()
        self.ui.sendMoneyAmountSpinBox.setValue(1)
        self.ui.sendMoneyConfirmPasswordLineEdit.clear()
        self.ui.depositAmountSpinBox.setValue(1)
        self.ui.depositConfirmPasswordLineEdit.clear()
        self.ui.withdrawAmountSpinBox.setValue(1)
        self.ui.withdrawConfirmPasswordLineEdit.clear()

        self.ui.errorSendMoneyLabel.clear()
        self.ui.errorDepositLabel.clear()
        self.ui.errorWithdrawLabel.clear()

        self.ui.stackedWidget.setCurrentIndex(4)

    def restore_or_maximize_app(self):
        if self.win_status == 0:
            self.showMaximized()
            self.win_status = 1
        else:
            self.showNormal()
            self.win_status = 0

    def deposit(self):
        if self.ui.depositConfirmPasswordLineEdit.text() == "":
            self.ui.errorDepositLabel.setText("Please Enter Password")
        elif self.ui.depositConfirmPasswordLineEdit.text() != return_password(self.account_number):
            self.ui.errorDepositLabel.setText("Incorrect Password")
        else:
            deposit(self.account_number, self.ui.depositAmountSpinBox.text().strip(' Birr'))
            self.ui.errorDepositLabel.setText("Deposited " + self.ui.depositAmountSpinBox.text() + " Successfully")
            # refresh the current amount in myAccount page
            self.ui.myAccountCurrentAmountLabel.setText(
                '<html><head/><body><p align="center"><span style=" font-size:12pt;'
                'font-weight:600;">' + return_current_amount(self.account_number)
                + ' Birr' + '</span></p></body></html>')

    def withdraw(self):
        if self.ui.withdrawConfirmPasswordLineEdit.text() == "":
            self.ui.errorWithdrawLabel.setText("Please Enter Password")
        elif self.ui.withdrawConfirmPasswordLineEdit.text() != return_password(self.account_number):
            self.ui.errorWithdrawLabel.setText("Incorrect Password")
        elif int(self.ui.withdrawAmountSpinBox.text().strip(' Birr')) > int(return_current_amount(self.account_number)):
            self.ui.errorWithdrawLabel.setText("Withdraw Amount Exceeds Deposit")
        else:
            withdraw(self.account_number, self.ui.withdrawAmountSpinBox.text().strip(' Birr'))
            self.ui.errorWithdrawLabel.setText("Withdrawn " + self.ui.withdrawAmountSpinBox.text() + " Successfully")
            # refresh the current amount in myAccount page
            self.ui.myAccountCurrentAmountLabel.setText(
                '<html><head/><body><p align="center"><span style=" font-size:12pt;'
                'font-weight:600;">' + return_current_amount(self.account_number)
                + ' Birr' + '</span></p></body></html>')

    def send(self):
        if self.ui.sendMoneyAccountNumberLineEdit.text() == "":
            self.ui.errorSendMoneyLabel.setText("Please Enter Receiver Account")
        elif self.ui.sendMoneyConfirmPasswordLineEdit.text() == "":
            self.ui.errorSendMoneyLabel.setText("Please Enter Password")
        elif self.ui.sendMoneyConfirmPasswordLineEdit.text() != return_password(self.account_number):
            self.ui.errorSendMoneyLabel.setText("Incorrect Password")
        elif os.path.exists("./data/" + str(self.ui.sendMoneyAccountNumberLineEdit.text())) is False:
            self.ui.errorSendMoneyLabel.setText("Account Does not exist")
        elif self.account_number == str(self.ui.sendMoneyAccountNumberLineEdit.text()):
            self.ui.errorSendMoneyLabel.setText("Cannot Send Money To Self")
        elif int(self.ui.sendMoneyAmountSpinBox.text().strip(' Birr')) > int(
                return_current_amount(self.account_number)):
            self.ui.errorWithdrawLabel.setText("Withdraw Amount Exceeds Deposit")
        else:
            send_money(self.account_number, self.ui.sendMoneyAccountNumberLineEdit.text(),
                       self.ui.sendMoneyAmountSpinBox.text().strip(' Birr'))
            self.ui.errorSendMoneyLabel.setText(
                "Sent " + self.ui.sendMoneyAmountSpinBox.text() + " to Account Number " +
                self.ui.sendMoneyAccountNumberLineEdit.text() + " Successfully")
            # refresh the current amount in myAccount page
            self.ui.myAccountCurrentAmountLabel.setText(
                '<html><head/><body><p align="center"><span style=" font-size:12pt;'
                'font-weight:600;">' + return_current_amount(self.account_number)
                + ' Birr' + '</span></p></body></html>')

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_DashBoardWindow()
        self.ui.setupUi(self)
        # make default buttons disappear
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.account_number = User.account_number
        # give function to close button
        close_button = self.ui.closeApp
        close_button.clicked.connect(lambda: self.close())

        # make minimize button
        minimize_button = self.ui.minimizeApp
        minimize_button.clicked.connect(lambda: self.showMinimized())

        # make maximize or restore
        self.ui.maximiseApp.clicked.connect(self.restore_or_maximize_app)

        # give function to the buttons on the left side
        self.ui.myAccountButton.clicked.connect(lambda: self.my_account_button())
        self.ui.sendMoneyButton.clicked.connect(lambda: self.send_money_button())
        self.ui.depositButton.clicked.connect(lambda: self.deposit_button())
        self.ui.withdrawButton.clicked.connect(lambda: self.withdraw_button())
        self.ui.aboutButton.clicked.connect(lambda: self.about_button())

        # set my account page's Labels
        self.ui.myAccountFirstNameLabel.setText('<html><head/><body><p align="center"><span style=" font-size:12pt; '
                                                'font-weight:600;">' + return_first_name(self.account_number)
                                                + '</span></p></body></html>')
        self.ui.myAccountLastNameLabel.setText('<html><head/><body><p align="center"><span style=" font-size:12pt; '
                                               'font-weight:600;">' + return_last_name(self.account_number)
                                               + '</span></p></body></html>')
        self.ui.myAccountAccountNumberLabel.setText('<html><head/><body><p align="center"><span style=" font-size:12pt;'
                                                    'font-weight:600;">' + self.account_number
                                                    + '</span></p></body></html>')
        self.ui.myAccountCurrentAmountLabel.setText('<html><head/><body><p align="center"><span style=" font-size:12pt;'
                                                    'font-weight:600;">' + return_current_amount(self.account_number)
                                                    + ' Birr' + '</span></p></body></html>')

        # change the look of the password placeholder
        self.ui.depositConfirmPasswordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.withdrawConfirmPasswordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.sendMoneyConfirmPasswordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        # give function to deposit, withdraw and send money button
        self.ui.depositDepositButton.clicked.connect(lambda: self.deposit())
        self.ui.withdrawWithdrawButton.clicked.connect(lambda: self.withdraw())
        self.ui.sendMoneySendButton.clicked.connect(lambda: self.send())


# TODO: connect the account_number for both of the windows
# TODO: make function for deposit and withdraw

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = SplashScreen()
    sys.exit(app.exec_())
