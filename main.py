import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class FilmInteraction(QMainWindow):
    def __init__(self, window):
        self.window = window
        super().__init__()
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()

    def load_ui(self):
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.comboBox.addItems(['Растворимый', 'Зерновой'])
        text = self.sender().text()
        if text == 'Добавить':
            self.setWindowTitle('Добавить элемент')
            self.add_btn.clicked.connect(lambda: self.coffee(text))
        elif text == 'Редактировать':
            if self.window.tableWidget.selectedItems():
                row = self.window.tableWidget.selectedItems()[0].row()
                id = self.window.tableWidget.item(row, 0).text()
                name = self.window.tableWidget.item(row, 1).text()
                degree = self.window.tableWidget.item(row, 2).text()
                gro_or_bea = self.window.tableWidget.item(row, 3).text()
                taste = self.window.tableWidget.item(row, 4).text()
                price = self.window.tableWidget.item(row, 5).text()
                size = self.window.tableWidget.item(row, 6).text()
                self.setWindowTitle('Редактирование записи')
                self.title_edit.setText(name)
                self.degree_edit.setText(degree)
                self.comboBox.setCurrentText(gro_or_bea)
                self.taste_edit.setText(taste)
                self.price_edit.setText(price)
                self.size_edit.setText(size)
                self.add_btn.clicked.connect(lambda: self.coffee(text, id))

    def coffee(self, i, id=None):
        try:
            title = self.title_edit.text()
            degree = self.degree_edit.text()
            bea_gro = self.comboBox.currentText()
            taste = self.taste_edit.text()
            price = self.price_edit.text()
            size = self.size_edit.text()
            if i == 'Добавить':
                id = sorted([i[0] for i in self.cur.execute('SELECT id FROM coffee').fetchall()])[-1]
                self.cur.execute(f'''INSERT INTO coffee(id, name, degree_roasting, ground_or_beans, taste_description, price, package_size)
                                 VALUES(?, ?, ?, ?, ?, ?, ?)''', (id + 1, title, degree, bea_gro, taste, price, size))
            else:
                self.cur.execute(f'''UPDATE coffee
                                         SET name = ?, degree_roasting = ?, ground_or_beans = ?, taste_description = ?, price = ?, package_size = ?
                                             WHERE id = ?''', (title, degree, bea_gro, taste, price, size, id))
            self.hide()
            self.con.commit()
            self.window.load_db()
        except Exception as ex:
            print(ex)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.load_db()
        for i in [self.add_btn, self.up_btn]:
            i.clicked.connect(lambda x: self.add_or_delete())

    def warn(self, text):
        QMessageBox.warning(self, "Предупреджение!",
                            text, QMessageBox.Ok)

    def info(self):
        QMessageBox.information(self, "Подсказка!",
                                'Вам необходимо выделить элемент который хотите изменить!',  QMessageBox.Ok)

    def add_or_delete(self):
        window = ex_2
        table = self.tableWidget
        if (self.sender().text() == 'Редактировать' and table.selectedItems()) or self.sender().text() == 'Добавить':
            window.show()
            window.load_ui()
        elif self.sender().text() == 'Редактировать' and not table.selectedItems():
            self.info()

    def load_db(self):
        res = self.con.cursor().execute('SELECT * FROM coffee').fetchall()
        table = self.tableWidget
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(['ИД', 'Название', 'Степень обжарки', 'Зерновой/растворимый', 'Вкус', 'Цена', 'Объем упаковки'])
        table.setRowCount(0)
        for i, row in enumerate(res):
            table.setRowCount(
                table.rowCount() + 1)
            for j, elem in enumerate(row):
                table.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    ex_2 = FilmInteraction(ex)
    sys.exit(app.exec())