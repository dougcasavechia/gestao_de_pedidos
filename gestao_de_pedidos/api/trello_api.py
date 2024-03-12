import requests
from datetime import datetime
import numpy as np
import os

class Trello_API:
    def __init__(
        self,
        base_path
        ):
        
        self.api_key = "6c0bb13a8d9be501e5905028f1cd839d"
        self.base_path = base_path
        
        self.trello_token_path = os.path.join(self.base_path, r'data\trello_token.txt')
        
        # Open the .txt file in read mode
        with open(self.trello_token_path, 'r') as file:
            # Read all lines from the file
            lines = file.readlines()

        self.trello_token = f"{lines[0]}"
    
    def create_new_card(
        self,
        important_infos,
        priority,
        date_to_liberate,
        list_id,
        project_files_links_list,
        payment_proof_links_list=None
        ):
        
        try:       
            method_error = None
            self.date_to_liberate = date_to_liberate
            self.priority = priority
            self.list_id = list_id
            
            url = f"https://api.trello.com/1/cards"
            
            files_links_to_drive = ""
            order_type = important_infos['Order_type']
            order_date = datetime.strptime(important_infos['Order_date'], '%d/%m/%Y')
            customer_id = str(important_infos['Customer_id']).zfill(4).strip()
            customer_name = important_infos['Customer_name'].strip()
            region = important_infos['Region'].strip()
            seller_name = important_infos['Seller_name'].strip()
            payment_method = important_infos['Payment_method'].strip()
            urgency = str(important_infos['Urgency']).strip()
            
            for i in range(len(project_files_links_list)):
                files_links_to_drive += f"\n**ARQUIVO {str(i+1).zfill(2)}** - {project_files_links_list[i]}"
            
            
            if order_type == "Z0" or order_type == "Z1":
            
                order_name = (
                    "# REP: "
                    f"{order_date.strftime('%y%m')}_"
                    f"{str(important_infos['Order_number']).zfill(4)} - "
                    f"{customer_name}"
                )
                
            elif urgency != None:
                order_name = (
                    "# URG: "
                    f"{order_date.strftime('%y%m')}_"
                    f"{str(important_infos['Order_number']).zfill(4)} - "
                    f"{customer_name}"
                )
            
            else:
                order_name = (
                    f"{order_date.strftime('%y%m')}_"
                    f"{str(important_infos['Order_number']).zfill(4)} - "
                    f"{customer_name}"
                )
            
            if payment_proof_links_list:
                order_description = (
                    f"**CLIENTE:** {customer_name} - **CÓD CLIENTE:** {str(customer_id).zfill(4)}"
                    f"\n**REGIÃO:** {region}"
                    f"\n**VENDEDOR:** {seller_name}"
                    f"\n**MÉTODO PGTO:** {payment_method}"
                    f"\n\n{files_links_to_drive}"
                    f"\n\n**PGTO:** {payment_proof_links_list[0]}"
                )
            else:
                order_description = (
                f"**CLIENTE:** {customer_name} - **CÓD CLIENTE:** {str(customer_id).zfill(4)}"
                f"\n**REGIÃO:** {region}"
                f"\n**VENDEDOR:** {seller_name}"
                f"\n\n{files_links_to_drive}"
            )
            
            query = {
                "name": f"{order_name}",
                "desc": order_description,
                "idList": self.list_id,
                "due": self.date_to_liberate + np.timedelta64(3, 'h'),
                "key": self.api_key,
                "token": self.trello_token
            }
            
            response_new_card = requests.request("POST", url, params=query)
        
            if self.priority == "URGENTE":
                color = "red"
            elif self.priority == "ALTA":
                color = "yellow"
            else:
                color = "blue"
        
            if response_new_card.status_code == 200:
                
                card_id = response_new_card.json()["id"]
                
                headers = {
                    "Accept": "application/json"
                }
            
                params = {
                    "key":  self.api_key,
                    "token": self.trello_token,
                    "value":{
                        'idAttachment': None,
                        'color': color,
                        'idUploadedBackground': None,
                        'size': 'normal',
                        'brightness': 'light'
                        }
                    }
                
                url_update_card = f"https://api.trello.com/1/cards/{card_id}/cover"

                requests.request("PUT", url_update_card, headers=headers, json=params)
                
            if response_new_card.status_code != 200:
                method_error = ("Erro ao criar um novo card no Trello! Tente novamente!"
                    f"\n\nSe o erro persistir, procure o resposável."
                    f"\n\nError: {response_new_card.text}"
                )
                
                return method_error           
            
            else:
                return method_error
            

        except Exception as error:
            #Others errors
            method_error = (f"An error occurred in method 'trello_api.create_new_card': {error}")
            
            return method_error
        
            