from api.googledrive_api import GoogleDrive_API
from api.trello_api import Trello_API
from utils.utils import Utils
from gui.gui import GUI
import tkinter as tk
import os
import sys

def main():       
    base_path = str(os.path.dirname(sys.executable))[:-5] if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
          
    googledrive_api_instance = GoogleDrive_API(base_path)
    trello_api_instance = Trello_API(base_path)
    utils_instance = Utils()

    # Criar uma instância de Tkinter
    root = tk.Tk()
          
    # Passar a instância de Tkinter para a classe GUI
    gui_instance = GUI(root, googledrive_api_instance, trello_api_instance, utils_instance, base_path)
    
    gui_instance.initiate_gui()

    # Iniciar o loop principal da interface gráfica
    root.mainloop()

if __name__ == "__main__":
    main()
