import requests
from bs4 import BeautifulSoup
import pandas as pd

def valuetoint(value_string):
    if value_string[-6:]=='mio. €':
        return int(float(value_string[:-7].replace(',','.'))*1e6)
    if value_string[-3:]=='K €':
        return int(float(value_string[:-4].replace(',','.'))*1e3)
    if value_string == "Transfert libre":
        return 0
    
def transformUrl(url_club,saison):
    test = url_club.split("/")
    new_url= "https://www.transfermarkt.fr/"+test[1]+"/transferrekorde/verein/"+test[4]+"/saison_id/"+str(saison)+"/pos//detailpos/0/w_s//altersklasse//plus/1"
    return new_url

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    
def getListTransfert(url_club,saison):
    
    page = transformUrl(url_club, saison)
    #♣page = "https://www.transfermarkt.fr"+url_club+"saison_id"+str(saison)+"/pos//detailpos/0/w_s//altersklasse//plus/1"
    #page = "https://www.transfermarkt.fr/fc-paris-saint-germain/transferrekorde/verein/583/saison_id/2021/pos//detailpos/0/w_s//altersklasse//plus/1"
    print(page)
    pageTree = requests.get(page, headers=headers)
    #print (pageTree)
    soup = BeautifulSoup(pageTree.content, 'html.parser')
    #print(soup)
    
    Liste_joueur = dict()
    Joueur = dict()

    index_joueur=1
    cond_sortie=False

    while (index_joueur <len( soup.find(id="yw1").find_all('tr'))) and (cond_sortie==False):
    #for index_joueur in range (1,len( soup.find(id="yw1").find_all('tr')),5):
        Joueur = dict()
        cond_sortie=True
        Players = soup.find(id="yw1").find_all('tr')[index_joueur].find_all('td')
        for i in range (len(Players)):
            if (i==1):
                Joueur["Nom"] = Players[i].find_all('td')[1].text.strip()
                Joueur["Joueur_lien"] =Players[i].find('a')['href']
                Joueur["Poste"] = Players[i].find_all('td')[2].text
            elif(i==5):
                Joueur["Age"] = int(Players[i].text)
            elif(i==6):
                Joueur["Nationalite"] =[]
                for nb_nat in Players[i].find_all('img'):
                    Joueur["Nationalite"] +=[nb_nat.get('title')]
            elif(i==7):
                Joueur["Club"] = Players[i].find('a').get('title')
                Joueur["Club_lien"] = Players[i].find('a')['href']
            elif(i==8):
                Joueur["Saison Transfert"] = Players[i].text
            elif(i==11):
                Joueur["Club d'arrivee"] = Players[i].text.strip()
                Joueur["Club d'arrivee lien"] = Players[i].find('a')['href']
            elif(i==12):
                Joueur["Championnat arrivee"] = Players[i].text.strip()
            elif(i==13):
                Joueur["VM transfert"] = valuetoint(Players[i].text.strip())
            elif(i==14):
                Joueur["Montant Transfert"] = valuetoint(Players[i].text)
                cond_sortie= (Players[i].text=="-")
        if cond_sortie==False:
            Liste_joueur[Joueur["Nom"]] = Joueur
            index_joueur+=5
            
    return Liste_joueur




    


Liste_joueur= getListTransfert("/fc-paris-saint-germain/startseite/verein/583", 2021)
print("\nJoueur")
print(Liste_joueur)
    

#soup=Players[3].find('a')

#print(soup['href'])P
"""i=0
match i :P
    case 0 :
        return 0"""
    
