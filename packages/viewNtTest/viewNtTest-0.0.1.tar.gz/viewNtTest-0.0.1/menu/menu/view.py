from tkinter import *
import webbrowser as wb
import os

try:
    OF_locat = sys._MEIPASS
except:
    OF_locat = ''

ressources = os.path.dirname(sys.argv[0])
class gui_window():

    def __init__(self,couleur = '#FFFFFF'):
        super().__init__()

        # config view
        self.couleur = couleur
        # Window
        self.window = Tk()
        self.menubar = Menu(self.window)
        self.window.wm_attributes("-topmost", 2)
        self.window.resizable(0,0)
        self.window.iconbitmap(os.path.join(OF_locat,"menu/img/favicon.png"))
        self.window.config(menu=self.menubar)


    def help(self):
        wb.open_new(os.path.join(ressources, r'.\doc\Instadoc.pdf'))

    def show(self):
        self.window.mainloop()

    def close(self):
        self.window.destroy()

if __name__ == '__main__':
    gui = gui_window()
    gui.show()