import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Utils:
    def __init__(self):
        pass

    def read_clipboard(self):
        '''Reads the content currently stored in the clipboard (CTRL+C) and creates a Pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the clipboard data.
        '''
        
        try:
            method_error = None
            dataframe = None
            
            self.datetime_current_date = datetime.now()
            self.current_date_np = np.datetime64(self.datetime_current_date)       
            self.int_day_current_date = pd.Timestamp(self.datetime_current_date).weekday()
            self.np_work_next_day = np.busday_offset(self.current_date_np.astype('datetime64[D]'), 1, roll='backward', weekmask='1111100')
            self.datetime_work_next_day = self.np_work_next_day.astype(datetime)
            self.int_day_next_work_date = pd.Timestamp(self.datetime_work_next_day).weekday()
            self.datetime_start_hour = timedelta(hours=8)
            self.np_start_hour = np.timedelta64(self.datetime_start_hour)
            self.datetime_finish_hour = timedelta(hours=18)
            self.np_finish_hour = np.timedelta64(self.datetime_finish_hour)
            self.np_start_time_next_work_day = self.np_work_next_day + self.np_start_hour
            self.np_finish_today_hour = np.busday_offset(self.current_date_np.astype('datetime64[D]'), 0, roll='backward', weekmask='1111100') + self.np_finish_hour
            
            dataframe = pd.read_clipboard()
            
            return dataframe, method_error
         
        except Exception as error:
            method_error = (f"An error occurred in method 'utils.read_clipboard': {error}")
            
            return dataframe, method_error



    def process_dataframe(self, dataframe:pd.DataFrame) -> dict:
        '''Process a DataFrame, extracting the necessary information.

        Args:
            dataframe (pd.DataFrame): DataFrame to be processed.

        Returns:
            dict: Dict of extracted information.
        '''

        try:
            method_error = None
            
            for index, row in dataframe.iterrows():
                self.infos_of = {
                    "Region": row["REGIAO"],
                    "Order_type": row["TIPO_OF"],
                    "Order_date": row["DATA_PED"],
                    "Order_number": str(row["NUMERO"]).zfill(4),
                    "Customer_name": row["NOME_FANTASIA"],
                    "Customer_id": row["CLIENTE"],
                    "Pay_condition": row["DESC_CONDPGTO"],
                    "Seller_name": row["NOME_VENDEDOR"],
                    "Company_stock": row["EMPRESA_ESTOQUE"],
                    "Payment_method" : row["DESC_CONDPGTO"],
                    "Urgency" : row["LIB_URG_OBS"]
                }
                
                return self.infos_of, method_error

        except Exception as error:
            method_error = (f"An error occurred in method 'utils.process_dataframe': {error}")
            self.infos_of = None
            
            return self.infos_of, method_error
    
    def verify_of_region_is_ok(self):
        self.region = self.infos_of.get("Region")
        
        self.dict_important_days = {   
            "1-SEGUNDA" : [3],
            "2-SEGUNDA" : [3],
            "1-TERCA"   : [],
            "2-TERCA"   : [2],
            "1-QUARTA"  : [],
            "2-QUARTA"  : [3],           
            "3-QUARTA"  : [3],
            "4-QUARTA " : [],
            "1-QUINTA"  : [1],
            "2-QUINTA"  : [4],
            "1-SEXTA"   : [],
            "2-SEXTA"   : [0],
            "RETIRA"    : [],
            "FABRICA"   : [],
            "FORA ROTA" : []
        }
        
        region_status = self.region in self.dict_important_days
               
        return region_status
    
    
    def verify_of_company_stock_is_ok(self):
        self.company_stock = self.infos_of.get("Company_stock")
        
        status_company_stock = True if self.company_stock == 1 else False
        
        return status_company_stock
    
    def get_list_in_trello(self):
        self.payment_method = self.infos_of.get("Payment_method")
        
        if self.payment_method == "ANTECIPADO":
            list_id_in_trello = "6560c2e0b5703f1330aaad43"
        else:
            list_id_in_trello = "6560bf6078e9dff5f4ef0a1a"
            
        return list_id_in_trello


    def define_order_priority(self):
        self.priority = None
        method_error = None
        
        try:
            important_day_region = self.dict_important_days.get(self.region)        

            # Priorities: 0 (maximum), 1 (high), 2 (normal)
            if (
                self.infos_of["Order_type"] == "Z0" or
                self.infos_of["Order_type"] == "Z1" or
                self.infos_of["Urgency"] != None or
                self.int_day_current_date in important_day_region
                ):

                # Set the priority
                self.priority = "URGENTE"    
                # Set the number of hours to add      
                self.hours_to_add = 0  # Change to the number of hours you want to add
                    
            elif self.int_day_next_work_date in important_day_region:
                # Set the priority
                self.priority = "ALTA"
                # Set the number of hours to add
                self.hours_to_add = 4  # Change to the number of hours you want to add

            else:
                # Set the priority
                self.priority = "NORMAL"
                # Set the number of hours to add
                self.hours_to_add = 8
                
            return self.priority, method_error

        except Exception as error:
            method_error = (f"An error occurred in method 'utils.define_order_priority': {error}")
            self.priority = None
            
            return self.priority, method_error
                
                
    def define_new_date_to_liberate(self):
        try:
            date_to_liberate = None
            method_error = None
            
            if self.datetime_current_date.hour >= 18:

                # Calculate the new date and time
                day_to_liberate = np.busday_offset(self.current_date_np.astype('datetime64[D]'), 1, roll='backward', weekmask='1111100')
                hour_to_liberate = self.np_start_hour + np.timedelta64(self.hours_to_add, 'h')
                
                date_to_liberate = day_to_liberate + hour_to_liberate
                
            elif self.datetime_current_date.hour < 8:
                day_to_liberate = np.busday_offset(self.current_date_np.astype('datetime64[D]'), 0, roll='backward', weekmask='1111100')
                hour_to_liberate = self.np_start_hour + np.timedelta64(self.hours_to_add, 'h')
                
                date_to_liberate = day_to_liberate + hour_to_liberate
                
            else:
                np_initial_date_to_liberate = self.current_date_np + np.timedelta64(self.hours_to_add, 'h')
                datetime_initial_date_to_liberate = np_initial_date_to_liberate.astype(datetime)
                
                datetime_initial_hour_to_liberate = datetime_initial_date_to_liberate.hour

                if datetime_initial_hour_to_liberate >= 18 or datetime_initial_hour_to_liberate < 8:
                    excess_time_today = np_initial_date_to_liberate - self.np_finish_today_hour
                    date_to_liberate = self.np_start_time_next_work_day + excess_time_today

                else:
                    date_to_liberate = np_initial_date_to_liberate

            return date_to_liberate, method_error
        
        except Exception as error:
            method_error = (f"An error occurred in method 'utils.define_new_date_to_liberate': {error}")
            date_to_liberate = None

            return date_to_liberate, method_error