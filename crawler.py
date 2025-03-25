#Datos necesarios:

''' FIJATE LAS IMPORTACIONES AUTOMATICAS QUE TE HACE '''
from asyncio import timeout


#Genero (gender)
#Apellido (last_name)
#Segundo apellido (second_name)
#Nombre (first_name)
#Segundo nombre (middle_name)
#DNI (id_numer)
#Fecha de Nacimiento (date_of_birth)
#Nacionalidad (nationality)
#Edad (age)
#Extraer la mayor informacion posible de cada individuo, en el caso de no contener un dato, directamente colocar N/A. El proyecto debera de contar con los siguientes archivos

##Cada vez que se actualiza la pagina coloca de manera diferente a las personas(Los va colocando de manera aleatoria)
 #A la hora de inspeccionar el codigo pulsar control + f y colocar lo siguiente en la casilla "col-sm-4" esto nos lleva a cada persona que esta en la pagina.
                                     #Datos solicitados
#Genero (gender)
#Apellido (last_name)
#Segundo apellido (second_name)
#Nombre (first_name)
#Segundo nombre (middle_name)
#DNI (id_numer)
#Fecha de Nacimiento (date_of_birth)
#Nacionalidad (nationality)
#Edad (age)
import re
import config
import requests
from bs4 import BeautifulSoup
import pandas as pd
'''El openpyxl no se importa, solo se lo instala y se lo usa'''
#import openpyxl
from datetime import datetime
from asyncio import timeout

class Crawler:
    def __init__(self):

        self.date_wanted = []
        self.profiles_links_data= []

    def wanted_unique_profile(self, soup1):
        try:
            wanted_data = soup1.find_all("div", class_="col-sm-12")

            for wanted in wanted_data:
                # Extraer datos correctamente
                gender_tag = wanted.find("label", attrs={"for": "GeneroId"})
                lastname_tag = wanted.find("label", attrs={"for": "Apellidos"})
                name_tag = wanted.find("label", attrs={"for": "Nombres"})
                birthdate_tag = wanted.find("label", attrs={"for": "FecNac"})
                document_tag = wanted.find("label", attrs={"for": "Documento"})
                nationality_tag = wanted.find("label", attrs={"for": "LugNac"})

                # Extraer valores correctamente
                gender = gender_tag.get_text(strip=True) if gender_tag else "None"
                lastname = lastname_tag.get_text(strip=True) if lastname_tag else "None"
                name = name_tag.get_text(strip=True) if name_tag else "None"
                birthdate = birthdate_tag.get_text(strip=True) if birthdate_tag else "None"
                document = document_tag.get_text(strip=True) if document_tag else "None"
                nationality = nationality_tag.get_text(strip=True) if nationality_tag else "None"

                # Procesar nombre
                if name and name != "None":
                    first_name, second_name = (name.split(maxsplit=1) + ["None"])[:2]
                else:
                    first_name, second_name = "None", "None"

                # Formatear ID
                id_number = re.sub(r"[.\-]", "", document) if document != "None" else "None"

                # Convertir fecha si es válida
                try:
                    meses = {
                        "ene": "Jan", "feb": "Feb", "mar": "Mar", "abr": "Apr", "may": "May", "jun": "Jun",
                        "jul": "Jul", "ago": "Aug", "sep": "Sep", "oct": "Oct", "nov": "Nov", "dic": "Dec"
                    }

                    for esp, eng in meses.items():
                        if esp in birthdate:
                            birthdate = birthdate.replace(esp, eng)
                            break

                    birthdate_obj = datetime.strptime(birthdate, "%d %b %Y").date()
                    birthdate_str = birthdate_obj.strftime("%Y-%m-%d")
                except ValueError:
                    birthdate_str = "N/A"

                # Guardar datos en diccionario
                wanted = {
                    "first_name": first_name,
                    "second_name": second_name,
                    "lastname": lastname,
                    "gender": gender,
                    "birthdate": birthdate_str,
                    "document": id_number,
                    "nationality": nationality
                }
                self.date_wanted.append(wanted)

                break  # Solo procesar el primer resultado
        except Exception as e:
            print(f"Hubo un error: {e}")

    def create_files(self):
        if len(self.date_wanted) != 0:
            df = pd.DataFrame(self.date_wanted)
            df.to_excel("date_wanted.xlsx", index=False, engine="openpyxl")
            df.to_csv('date_wanted.csv', index=False, encoding='utf-8')
            print("Archivos creados")
        else:
            print("Error, no hay datos para guardar")


    def get_information_profile(self):
        try:
            '''Recorda que la variable soup es local, por lo que no hay problema si quieres volver a poner
                 response
                 soup
               Solo es una aclaracion, no hay error aqui
            '''
            for profile in self.profiles_links_data:
                response_1 = requests.get(f"{profile}", headers=config.HEADERS, timeout=100)
                soup1 = BeautifulSoup(response_1.text, "html.parser")
                #print(f"Esto es lo que imprime en soup1 {soup1}")
                self.wanted_unique_profile(soup1)
        except Exception as e:
            print(f"Erro al solicitar la informacion de {e}")



    def scraping_profile(self,soup):
        try:

            '''Recorda eliminar los comentarios, el codigo final debe de quedar limpio, da mal aspecto'''

            profiles = soup.find_all("div", class_="col-sm-4")
            for card in profiles:
                profile_link_data = card.find("div", class_= "panel-body").find("a").attrs.get("href")
                profile_link_data_single = config.BASE_URL_PROFILE+profile_link_data
                self.profiles_links_data.append(profile_link_data_single)
        except Exception as e:
            print(f"Error al extraer  la informacion: {e}")


    def get_all_information(self):
        try:
            response = requests.get(f"{config.BASE_URL_PAGE}", headers=config.HEADERS, timeout=100)
            soup = BeautifulSoup(response.text, "html.parser")
            self.scraping_profile(soup)
        except Exception as e:

            '''Acordate de imprimir el error, para un mejor comprension del mismo'''
            print(f"Error al intentar solicitar la informacion: {e}")


    def run(self):
        self.get_all_information()
        self.get_information_profile()
        #self.create_files()
        return  None



'''################### No agregaste el archivo requirements.txt, agregalo #####################'''

if __name__== "__main__":
    crawler = Crawler()
    crawler.run()

