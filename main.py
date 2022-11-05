from PySide6.QtWidgets import QApplication
import widgets

def main():
    app = QApplication([])
    window = widgets.MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()