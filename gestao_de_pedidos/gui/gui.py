import tkinter as tk
from tkinter import messagebox, Label
from PIL import Image, ImageTk
import os


class GUI:
    def __init__(self,
                root,
                googledrive_api_instance,
                trello_api_instance,
                utils_instance,
                base_path
                ):

        self.googledrive_api_instance = googledrive_api_instance
        self.trello_api_instance = trello_api_instance
        self.utils_instance = utils_instance
        
        self.base_path = base_path
        self.root = root
        
        # Set up the main window
        self.root.title("Gerenciador de Pedidos - Realbox")
        self.root.geometry("520x520")
        self.root.configure(bg="#A01117")
        
        self.icon_path = os.path.join(self.base_path, r'data\realbox-ico.ico')
        self.root.iconbitmap(self.icon_path)
        
        # Possible sellers errors
        self.dict_sellers_errors = {
            "ERROR_ONLY_ONE_OF" : "Apenas uma OF pode ser selecionada por vez. Exporte novamente a informação com apenas uma OF!",
            "ERROR_INVALID_REGION" : "A região da OF não é uma região válida. Certifique-se de corrigir a OF e inicie o processo novamente!",
            "ERROR_INVALID_COMPANY_STOCK" : "A empresa-estoque está errada. Pode não aparecer as peças em PCP. Certifique-se de corrigir a OF e inicie o processo novamente!",
            "ERROR_EXPORTED_DATA": "Houve um erro com os dados exportados. Certifique que exportou os dados corretamente e tente novamente!"
        }
         
    def initiate_gui(self):
        try:
            method_error = self.googledrive_api_instance.validate_google_token()
            if not method_error:
                # Insert logo in program
                self.insert_logo()
                
                # Buttons
                self.create_buttons()

                # Place buttons using the place method
                self.place_buttons()
                
                # Change mouse when the mouse is on
                self.configure_cursor_on_buttons()
            
            else:
                messagebox.showinfo(
                    f"##### ERRO #####",
                    f"{method_error}"
                )
                
                self.root.destroy()
        
                
        except Exception as error:
            method_error = (f"An error occurred in method 'gui.initiate_gui': {error}")

            messagebox.showinfo(
                f"##### ERRO #####",
                f"{method_error}"
            )
            
            self.root.destroy()
            
    def insert_logo(self):
        self.image_1_path = os.path.join(self.base_path, r'data\realbox-logo.png')
        self.image_2_path = os.path.join(self.base_path, r'data\realbox-logo2.png')
        
        
        # Carrega a imagem (no formato PNG)
        image_1 = ImageTk.PhotoImage(Image.open(f"{self.image_1_path}"))
        image_2 = ImageTk.PhotoImage(Image.open(f"{self.image_2_path}"))

        '''LOGO SUPERIOR'''
        # Cria um Label e configura a imagem
        label_logo_1 = Label(self.root, image=image_1)
        label_logo_1.image = image_1  # Mantem uma referência para a imagem para evitar a coleta de lixo
        
        # Posiciona e configura o Label com transparência
        label_logo_1.place(x=260, y=70, anchor="center", width=250, height=115)
        label_logo_1.configure(bg=self.root.cget('bg'))
        
        '''LOGO INFERIOR'''
        label_logo_2 = Label(self.root, image=image_2)
        label_logo_2.image = image_2  # Mantem uma referência para a imagem para evitar a coleta de lixo
        
        # Posiciona e configura o Label com transparência
        label_logo_2.place(x=260, y=485, anchor="center", width=250, height=50)
        label_logo_2.configure(bg=self.root.cget('bg'))

            
    def create_buttons(self):
        self.btn_start = tk.Button(
            self.root,
            text="NOVO PROJETO",
            command=self.new_project,
            font=("Tahoma", 12, "bold"),
            bg="white"
        )
        
        self.btn_export_data = tk.Button(
            self.root,
            text="EXPORTAR DADOS",
            command=self.read_infos_clipboard,
            font=("Tahoma", 12, "bold"), 
            bg="white",
            state=tk.DISABLED
        )
        
        self.btn_upload_project_file = tk.Button(
            self.root,
            text="CARREGAR ARQUIVO 01",
            command=self.read_file_project_clipboard,
            font=("Tahoma", 12, "bold"),
            bg="white",
            state=tk.DISABLED
        )
        
        self.btn_upload_payment_proof_file = tk.Button(
            self.root,
            text="COMPROVANTE PGTO",
            command=self.read_file_payment_proof_clipboard,
            font=("Tahoma", 12, "bold"),
            bg="white",
            state=tk.DISABLED
        )  
        
        self.btn_end = tk.Button(
            self.root,
            text="FINALIZAR PROJETO",
            command=self.end_project,
            font=("Tahoma", 12, "bold"),
            bg="white",
            state=tk.DISABLED
        )     
        
    
    def place_buttons(self):
        self.btn_start.place(
            x=260,
            y=170,
            anchor="center",
            width=250,
            height=50
        )
        
        self.btn_export_data.place(
            x=260,
            y=240,
            anchor="center",
            width=250,
            height=50
        )
        
        self.btn_upload_project_file.place(
            x=260,
            y=295,
            anchor="center",
            width=250,
            height=50
        )
        
        self.btn_upload_payment_proof_file.place(
            x=260,
            y=350,
            anchor="center",
            width=250,
            height=50
        )
        
        self.btn_end.place(
            x=260,
            y=420,
            anchor="center",
            width=250,
            height=50
        )
        
    def configure_cursor_on_buttons(self):
        self.btn_start.bind("<Enter>", lambda event: self.change_cursor(event, "hand2"))
        self.btn_start.bind("<Leave>", lambda event: self.change_cursor(event, ""))
        
        self.btn_export_data.bind("<Enter>", lambda event: self.change_cursor(event, "hand2"))
        self.btn_export_data.bind("<Leave>", lambda event: self.change_cursor(event, ""))
        
        self.btn_upload_project_file.bind("<Enter>", lambda event: self.change_cursor(event, "hand2"))
        self.btn_upload_project_file.bind("<Leave>", lambda event: self.change_cursor(event, ""))
        
        self.btn_upload_payment_proof_file.bind("<Enter>", lambda event: self.change_cursor(event, "hand2"))
        self.btn_upload_payment_proof_file.bind("<Leave>", lambda event: self.change_cursor(event, ""))

        self.btn_end.bind("<Enter>", lambda event: self.change_cursor(event, "hand2"))
        self.btn_end.bind("<Leave>", lambda event: self.change_cursor(event, ""))


    def change_cursor(self, event, cursor_type):
        event.widget.config(cursor=cursor_type)

        
    def new_project(self):
        # Starting new program and variables
        self.upload_counter = 1
        self.image_link = None
        self.project_files_links_list = []
        self.payment_proof_links_list = []
        self.enable_only_export_data_button()
        

    def read_infos_clipboard(self):
        dataframe_exported_data, method_error = self.utils_instance.read_clipboard()

        if not method_error:
                        
            if len(dataframe_exported_data) == 1:
                self.infos_of, method_error = self.utils_instance.process_dataframe(dataframe_exported_data)

                if not method_error:
                    status_region = self.utils_instance.verify_of_region_is_ok()
                    status_company_stock = self.utils_instance.verify_of_company_stock_is_ok()

                    if status_region:

                        if status_company_stock:
                            self.priority, method_error = self.utils_instance.define_order_priority()
                            
                            if not method_error:
                                self.date_to_liberate, method_error = self.utils_instance.define_new_date_to_liberate()
                                
                                if not method_error:
                                    self.folder_id_of, method_error = self.googledrive_api_instance.verify_folders(self.infos_of['Order_date'], self.infos_of['Order_number'])
                                    self.enable_only_upload_project_file_button()  # Enable upload file button
                                    
                                    if self.infos_of['Payment_method'] == 'ANTECIPADO':
                                        self.btn_upload_payment_proof_file["state"] = tk.NORMAL
                                        self.pressed_button = False
                                        
                                    else:
                                        self.btn_upload_payment_proof_file["state"] = tk.DISABLED
                                        self.pressed_button = True
                                    
                                    return self.infos_of

                                else:
                                    self.enable_only_new_project_button()
                                    self.show_error_message(method_error)
                                    
                            else:
                                self.enable_only_new_project_button()
                                self.show_error_message(method_error) 
                    
                        else:
                            self.enable_only_new_project_button()
                            self.show_error_message(self.dict_sellers_errors["ERROR_INVALID_COMPANY_STOCK"])

                    else:
                        self.enable_only_new_project_button()
                        self.show_error_message(self.dict_sellers_errors["ERROR_INVALID_REGION"])

                else:
                    self.enable_only_new_project_button()
                    self.show_error_message(method_error)

            elif len(dataframe_exported_data) > 1:
                self.enable_only_new_project_button()
                self.show_error_message(self.dict_sellers_errors["ERROR_MORE_THAN_ONE_EXPORTED_DATA"])

            else:
                self.enable_only_new_project_button()
                self.show_error_message(self.dict_sellers_errors["ERROR_EXPORTED_DATA"])

        else:
            self.enable_only_new_project_button()
            self.show_error_message(method_error)


    def read_file_project_clipboard(self):

        self.image_link = None
        calling_method = "read_file_project_clipboard"
        
        self.image_link, method_error = self.googledrive_api_instance.upload_file_to_drive(
            self.folder_id_of, self.infos_of, self.upload_counter, calling_method
        )

        if not method_error:
            self.upload_counter += 1
            self.btn_end["state"] = tk.NORMAL
            self.btn_upload_project_file["text"] = f"CARREGAR ARQUIVO {str(self.upload_counter).zfill(2)}"
            self.project_files_links_list.append(self.image_link)
            
            return self.project_files_links_list
        
        else:
            self.show_error_message(method_error)
            
    def read_file_payment_proof_clipboard(self):
        self.payment_proof_link = None
        calling_method = "read_file_payment_proof_clipboard"
        
        self.payment_proof_link, method_error = self.googledrive_api_instance.upload_file_to_drive(
            self.folder_id_of, self.infos_of, self.upload_counter, calling_method
        )

        if not method_error:
            self.btn_upload_payment_proof_file["state"] = tk.DISABLED
            self.payment_proof_links_list.append(self.payment_proof_link)
            self.pressed_button = True
            
            return self.payment_proof_links_list
        
        else:
            self.show_error_message(method_error)

    
    def end_project(self):
        if self.pressed_button:
            list_id = self.utils_instance.get_list_in_trello()
            
            method_error = self.trello_api_instance.create_new_card(
            self.infos_of,
            self.priority,
            self.date_to_liberate,
            list_id,
            self.project_files_links_list,
            self.payment_proof_links_list
            )

            if not method_error:   
                messagebox.showinfo(
                    f"OF {self.infos_of['Order_number']} - {self.priority}",
                    f"Código: {self.infos_of['Customer_id']}" + \
                    f"\nCliente: {self.infos_of['Customer_name']}" + \
                    f"\nRegião: {self.infos_of['Region']}" + \
                    f"\n\nMétodo de Pagamento: {self.infos_of['Payment_method']}"
                )
                
                self.upload_counter = 1
                self.btn_upload_project_file["text"] = f"CARREGAR ARQUIVO {str(self.upload_counter).zfill(2)}"
                self.enable_only_new_project_button()
                
            else:
                self.show_error_message(method_error)
        else:
            self.show_error_message("É necessário adicionar um comprovante de pagamento para esse cliente. Copie o comprovante e tente novamente.")

    def enable_only_new_project_button(self):
        self.btn_start["state"] = tk.NORMAL
        self.btn_export_data["state"] = tk.DISABLED
        self.btn_upload_project_file["state"] = tk.DISABLED
        self.btn_upload_payment_proof_file["state"] = tk.DISABLED
        self.btn_end["state"] = tk.DISABLED
        
        
    def enable_only_export_data_button(self):
        self.btn_start["state"] = tk.DISABLED
        self.btn_export_data["state"] = tk.NORMAL
        self.btn_upload_project_file["state"] = tk.DISABLED
        self.btn_upload_payment_proof_file["state"] = tk.DISABLED
        self.btn_end["state"] = tk.DISABLED
        

    def enable_only_upload_project_file_button(self):
        self.btn_start["state"] = tk.DISABLED
        self.btn_export_data["state"] = tk.DISABLED
        self.btn_upload_project_file["state"] = tk.NORMAL
        self.btn_end["state"] = tk.DISABLED


    def show_error_message(self, method_error):
        messagebox.showinfo("### ATENÇÃO ###", method_error) 