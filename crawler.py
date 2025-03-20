#Datos necesarios:
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




import config
import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
from datetime import datetime


class Crawler:
    def __init__(self):

        self.date_wanted = []
        self.profiles_links_data= []

    def wanted_unique_profile(self, soup1):
        try:
            wanted_data = soup1.find_all("div", class_="col-sm-12")

            for wanted in wanted_data:
                # Extraemos los datos del HTML y asignamos "N/A" si no existen
                gender = wanted.find("label", attrs={"for": "GeneroId"}).next_sibling or "N/A"
                lastname = wanted.find("label", attrs={"for": "Apellidos"}).next_sibling or "N/A"
                name = wanted.find("label", attrs={"for": "Nombres"}).next_sibling or "N/A"
                birthdate = wanted.find("label", attrs={"for": "FecNac"}).next_sibling or "N/A"
                document = wanted.find("label", attrs={"for": "Documento"}).next_sibling or "N/A"
                nationality = wanted.find("label", attrs={"for": "LugNac"}).next_sibling or "N/A"

                # Limpiamos los datos eliminando ":" y espacios extra
                gender = gender.replace(":", "").strip()
                lastname = lastname.replace(":", "").strip()
                name = name.replace(":", "").strip()
                birthdate = birthdate.replace(":", "").strip()
                document = document.replace(":", "").strip()
                nationality = nationality.replace(":", "").strip()

                try:
                    # Mapeo de meses en español a inglés
                    meses = {
                        "ene": "Jan", "feb": "Feb", "mar": "Mar", "abr": "Apr", "may": "May", "jun": "Jun",
                        "jul": "Jul", "ago": "Aug", "sep": "Sep", "oct": "Oct", "nov": "Nov", "dic": "Dec"
                    }

                    for esp, eng in meses.items():
                        if esp in birthdate:
                            birthdate = birthdate.replace(esp, eng)
                            break

                    birthdate = datetime.strptime(birthdate, "%d %b %Y").date()
                    birthdate_str = birthdate.strftime("%d/%m/%Y")

                except ValueError:
                    birthdate_str = "N/A"  # Si la fecha no se puede convertir, dejamos "N/A"

                # Diccionario con los datos requeridos
                wanted = {
                    "name": name,
                    "lastname": lastname,
                    "gender": gender,
                    "birthdate":birthdate_str ,
                    "document": document,
                    "nationality": nationality
                }
                self.date_wanted.append(wanted)
                print(f"Esto es el producto: {wanted}")
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
            for profile in self.profiles_links_data:
                response_1 = requests.get(f"{profile}", headers=config.HEADERS, timeout=100)
                soup1 = BeautifulSoup(response_1.text, "html.parser")
                #print(f"Esto es lo que imprime en soup1 {soup1}")
                self.wanted_unique_profile(soup1)
        except Exception as e:
            print(f"Erro al solicitar la informacion de {e}")



    def scraping_profile(self,soup):
        try:
            profiles = soup.find_all("div", class_="col-sm-4")
            #print(profiles[0])
            for card in profiles:
                profile_link_data = card.find("div", class_= "panel-body").find("a").attrs.get("href")
                #print(f"Link de perfil encontrado: {config.BASE_URL_PROFILE}{profile_link_data}")
                profile_link_data_single = config.BASE_URL_PROFILE+profile_link_data
                #print(f"Esto es lo que tengo en profile_link_data_single{profile_link_data_single}")
                #self.get_information_profile(profile_link_data_single)
                self.profiles_links_data.append(profile_link_data_single)
        except Exception as e:
            print(f"Error al extraer  la informacion: {e}")


    def get_all_information(self):
        try:
            response = requests.get(f"{config.BASE_URL_PAGE}", headers=config.HEADERS, timeout=100)
            soup = BeautifulSoup(response.text, "html.parser")
            self.scraping_profile(soup)
        except:
            print("Error al intentar solicitar la informacion")


    def run(self):
        self.get_all_information()
        self.get_information_profile()
        self.create_files()
        return  None


if __name__== "__main__":
    crawler = Crawler()
    crawler.run()



