from datetime import datetime
import locale
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
from PIL import Image, ImageGrab

class GoogleDrive_API:
  def __init__(self, base_path):
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    self.datetime_current_date = datetime.now()
    self.SCOPES = ["https://www.googleapis.com/auth/drive"]
    self.base_path = base_path
    self.root_folder_id = "1JDGBv6PnwX-3M_ZbpEXTJSPg4j27j_5E"

  def validate_google_token(self):
    '''' The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first time.
    '''
      
    try:
      method_error = None
      self.creds = None
      token_path = os.path.join(self.base_path, r'token.json')
      credentials_path = os.path.join(self.base_path, r'data\credentials.json')
      
      if os.path.exists(token_path):
        self.creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.

      if not self.creds or not self.creds.valid:
        if self.creds and self.creds.expired and self.creds.refresh_token:
          self.creds.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path , self.SCOPES
          )
          self.creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, "w") as token:
          token.write(self.creds.to_json())
      
      return method_error

    except FileNotFoundError as error:
      # Error file not found
      method_error = ("Arquivo 'token.json' não encontrado. Abra o programa novamente."
        f"\n\nSe o erro persistir, procure o resposável."
        f"\n\nError: {error}"
      )
      
      return method_error

    except Exception as error:
      #Others errors
      method_error = (f"An error occurred in method 'google_api.validate_google_token': {error}")
        
      return method_error

        
  def search_folder(self, search_name, folder_id) -> str:
    ''' This function searches for a folder in two different ways: one when no parameters are provided and another when an ID is provided. 
    If no parameters are provided, it searches for the desired folder name in the root of the drive. 
    If an ID is provided, it searches for the desired folder name within the specified folder.
    '''  
    try:
      self.service = build('drive', 'v3', credentials=self.creds)
      folder_id_result = None
      method_error = None
      
      query = f"mimeType='application/vnd.google-apps.folder' and name='{search_name}' and '{folder_id}' in parents" 

      response = (self.service.files().list(q=query, spaces="drive").execute())

      for folder in response.get('files', []):
        folder_id_result = folder.get("id")

      return folder_id_result, method_error
    
    except HttpError as error:
      method_error = (f"An error occurred in method 'google_api.search_folder': {error}")
      
      return folder_id_result, method_error


  def create_folder(self, folder_name, parent_folder_id=None):
    ''' This function creates a folder in two different ways: 
    one when no parent_folder_id is provided (creates the folder in the root of the drive),
    and another when an ID is provided (creates the folder in the specified folder).
    '''
    method_error = None
    
    # Preparing file metadata
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_folder_id]
    }
    
    # file_metadata["parents"] = [parent_folder_id]  # Ensure parents is a list
    
    try:
      created_folder = self.service.files().create(body=file_metadata, fields="id").execute()
      created_folder_id = created_folder.get('id')
      
      return created_folder_id, method_error
      
    except HttpError as method_error:
      print(f"An error occurred: {method_error}")
      created_folder_id = None
      
      return created_folder_id, method_error
      
    except Exception as method_error:
      print(f"An error occurred: {method_error}")
      created_folder_id = None
      
      return created_folder_id, method_error

  def upload_file_to_drive(self, folder_id: str, of_infos: dict, file_number: int, calling_method: str):
      if not folder_id:
        return None, "Folder ID não fornecido. O upload requer um ID de pasta válido."

      try:
        file_link = None
        file_bytes, mimetype, file_extension = self.get_file_from_clipboard()
        
        if file_bytes is None:
          return None, "Não foi copiado um arquivo válido (imagem, PDF, DOC, DOCX, XLS, XLSX). Tente novamente."

        file_name = self.generate_file_name(calling_method, of_infos, file_number, file_extension)

        print(f"Folder_ID da pasta para upar: {folder_id}")
        
        # Prepara metadados e faz o upload do arquivo
        file_metadata = {"name": file_name, "parents": [folder_id]}
        media = MediaIoBaseUpload(file_bytes, mimetype=mimetype)
        file = self.service.files().create(body=file_metadata, media_body=media, fields="webViewLink").execute()
        file_link = file.get("webViewLink")

        return file_link, None

      except Exception as error:
        return None, f"Ocorreu um erro ao fazer upload do arquivo: {error}"

      finally:
        if isinstance(file_bytes, BytesIO):
          file_bytes.close()

  def get_file_from_clipboard(self):
    file_clipboard = ImageGrab.grabclipboard()

    # Verifica se é uma imagem diretamente na área de transferência
    if isinstance(file_clipboard, Image.Image):
      return self.save_image_to_bytes(file_clipboard), "image/jpeg", "jpg"

    # Verifica se o conteúdo é uma lista com um caminho de arquivo
    elif isinstance(file_clipboard, list) and len(file_clipboard) == 1 and os.path.isfile(file_clipboard[0]):
      file_path = file_clipboard[0]
      if self.is_image_file(file_path):
        # Se o arquivo for uma imagem, baseando-se na extensão
        image = Image.open(file_path)
        return self.save_image_to_bytes(image), "image/jpeg", "jpg"
      else:
        # Se o arquivo não for uma imagem, mas ainda é um arquivo válido
        return self.open_file(file_path)

    return None, None, None

  def save_image_to_bytes(self, image):
      file_bytes = BytesIO()
      image.save(file_bytes, format="JPEG")
      file_bytes.seek(0)
      
      return file_bytes

  def open_file(self, file_path):
      file_extension = os.path.splitext(file_path)[-1].lower()
      mimetype = self.get_mimetype_by_extension(file_extension)
      if mimetype:
          with open(file_path, "rb") as file:
              file_bytes = BytesIO(file.read())
              file_bytes.seek(0)
          return file_bytes, mimetype, file_extension.lstrip('.')
      else:
          return None, None, None

  def get_mimetype_by_extension(self, extension):
      mimetypes = {
          ".pdf": "application/pdf",
          ".doc": "application/msword",
          ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
          ".xls": "application/vnd.ms-excel",
          ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          ".png": "image/png",
          ".jpg": "image/jpeg",
          ".jpeg": "image/jpeg",
          ".tiff": "image/tiff",
          ".bmp": "image/bmp",
          ".gif": "image/gif"
      }
      return mimetypes.get(extension)

  def is_image_file(self, file_path):
      # Verifica a extensão do arquivo para determinar se é uma imagem
      image_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']
      file_extension = os.path.splitext(file_path)[-1].lower()
      return file_extension in image_extensions

  def generate_file_name(self, calling_method, of_infos, file_number, file_extension):
    if calling_method == "read_file_project_clipboard":
      base_name = f"{datetime.strptime(of_infos['Order_date'], '%d/%m/%Y').strftime('%y%m')}_{of_infos['Order_number']}_{str(file_number).zfill(2)}"
    elif calling_method == "read_file_payment_proof_clipboard":
      base_name = f"PGTO_{datetime.strptime(of_infos['Order_date'], '%d/%m/%Y').strftime('%y%m')}_{of_infos['Order_number']}"
    else:
      base_name = "Uploaded_File"
    return f"{base_name}.{file_extension}"

  # def upload_file_to_drive(self, folder_id: str, of_infos: dict, file_number: int, calling_method: str) -> str:
  #   try:
  #     method_error = None
  #     file_link = None
      
  #     print(folder_id)

  #     file_clipboard = ImageGrab.grabclipboard()

  #     # Se uma imagem é copiada diretamente para a área de transferência
  #     if isinstance(file_clipboard, Image.Image):
  #       file_bytes = BytesIO()
  #       file_clipboard.save(file_bytes, format="JPEG")
  #       mimetype = "image/jpeg"
  #       file_extension = "jpg"
  #       file_bytes.seek(0)

  #     # Se um arquivo é copiado (lista com caminho de arquivo)
  #     elif isinstance(file_clipboard, list) and len(file_clipboard) == 1 and os.path.isfile(file_clipboard[0]):
  #       file_path = file_clipboard[0]
  #       file_extension = os.path.splitext(file_path)[-1].lower()
        
  #       if file_extension in [".pdf", ".doc", ".docx", ".xls", ".xlsx"]:
  #         file_bytes = open(file_path, "rb")
  #         if file_extension == ".pdf":
  #           mimetype = "application/pdf"
  #         elif file_extension == ".doc":
  #           mimetype = "application/msword"
  #         elif file_extension == ".docx":
  #           mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
  #         elif file_extension == ".xls":
  #           mimetype = "application/vnd.ms-excel"
  #         elif file_extension == ".xlsx":
  #           mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  #       else:
  #         # Tratamento padrão para outros formatos de imagem
  
  #         file = Image.open(file_path)
  #         file_bytes = BytesIO()
  #         file.save(file_bytes, format="JPEG")
  #         file_bytes.seek(0)
  #         mimetype = "image/jpeg"
  #         file_extension = "jpg"

  #     else:
  #       method_error = "Não foi copiado um arquivo válido (imagem, PDF, DOC, DOCX, XLS, XLSX). Tente novamente."
  #       file_link = None

  #     # Define o nome do arquivo baseado no método de chamada e nas informações fornecidas
  #     if calling_method == "read_file_project_clipboard":
  #       file_name = f"{datetime.strptime(of_infos['Order_date'], '%d/%m/%Y').strftime('%y%m')}_{of_infos['Order_number']}_{str(file_number).zfill(2)}"
  #     elif calling_method == "read_file_payment_proof_clipboard":
  #       file_name = f"PGTO_{datetime.strptime(of_infos['Order_date'], '%d/%m/%Y').strftime('%y%m')}_{of_infos['Order_number']}"
  #     else:
  #       file_name = "Uploaded_File"

  #     print(f"Folder_ID da pasta para upar: {folder_id}")
      
  #     # Prepara metadados e faz o upload do arquivo
  #     media = MediaIoBaseUpload(file_bytes, mimetype=mimetype)
  #     file_metadata = {
  #       "name": f"{file_name}.{file_extension.lstrip('.')}",
  #       "parents": [folder_id]
  #     }

  #     file = self.service.files().create(body=file_metadata, media_body=media, fields="webViewLink").execute()
  #     file_link = file.get("webViewLink")
      
  #     return file_link, method_error

  #   except Exception as error:
  #     method_error = f"Ocorreu um erro ao fazer upload do arquivo: {error}"
  #     file_link = None

  #     return file_link, method_error


  def verify_folders(self, order_date, order_number):
    folder_id_year_and_month = None
    folder_id_day = None
    folder_id_of = None
    method_error = None
    
    self.order_date = datetime.strptime(order_date, "%d/%m/%Y")
    self.order_number = order_number
    
    try:
      folder_name_year_and_month = self.order_date.strftime("%Y-%m / %B de %Y").encode('latin-1').decode('utf-8')
      folder_name_day = self.order_date.strftime("%Y/%m/%d - %d de %B de %Y").encode('latin-1').decode('utf-8')
      folder_name_of = f"OF {order_number}_{self.order_date.strftime('%y%m')}"

      # Verifica e cria pasta do ano e mês, se necessário
      folder_id_year_and_month, method_error = self.search_folder(folder_name_year_and_month, self.root_folder_id)
      if method_error:
        return None, method_error
      if not folder_id_year_and_month:
        folder_id_year_and_month, method_error = self.create_folder(folder_name_year_and_month, self.root_folder_id)
        if method_error:
          return None, method_error

      # Verifica e cria pasta do dia, se necessário
      folder_id_day, method_error = self.search_folder(folder_name_day, folder_id_year_and_month)
      if method_error:
        return None, method_error
      if not folder_id_day:
        folder_id_day, method_error = self.create_folder(folder_name_day, folder_id_year_and_month)
        if method_error:
          return None, method_error

      # Verifica e cria pasta da OF, se necessário
      folder_id_of, method_error = self.search_folder(folder_name_of, folder_id_day)
      if method_error:
        return None, method_error
      if not folder_id_of:
        folder_id_of, method_error = self.create_folder(folder_name_of, folder_id_day)
        if method_error:
          return None, method_error
          
      return folder_id_of, method_error

    except Exception as error:
      method_error = f"An error occurred in method 'verify_folders': {error}"
      return None, method_error
    

