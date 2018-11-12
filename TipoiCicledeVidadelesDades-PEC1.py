#PEC Tipologia i cicle de vida de les dades
#Propietat de la UOC i l'alumne Josep Consuegra Navarrina
#12/11/2018
#Released Under CC BY-NC-SA 4.0 License


#Importem les llibreries necessàries
import requests
from bs4 import BeautifulSoup
import builtwith
import numpy as np
import pandas as pd
import whois
import datetime

#Obtenim detalls de la pàgina web a descarregar
builtwith.parse('https://www.pompeiibrand.com/')
print(whois.whois('pompeiibrand.com'))

#definim la primera url que volem tractar amb la llibreria beautifulSoup
url='https://www.pompeiibrand.com/collections/zapatillas-hombre'
page=requests.get(url)
soupman=BeautifulSoup(page.content)

#definim el dataframe per emmagatzemar les dades
df=pd.DataFrame(columns=['Data','Marca','Gènere','Model','Color','Oferta','Preu', 'Talla'])

#generem la data del sistema per a temporalitzar l'extracció
now=datetime.datetime.now()
date=str(now.year)+'/'+str(now.month)+'/'+str(now.day)

#Scrapejem el contigut de la pàgina descarregada per a la categoria 'Home'
for collection in soupman.body.find_all('div',attrs={'class':'single-collection'}):
    shoe = collection.find('div',attrs={'class':'grid__item'}).h3
    for item in collection.find_all('a',attrs={'class':'grid-view-item__link'}):
        color=item.find('div',attrs={'class':'h4'}).span
        model=item.find('div',attrs={'class':'grid-view-item__meta'}).span
        sizes=item.find('div',attrs={'class':'sizes-wrap'})
        if sizes is not None:
            length=sizes.findChildren('span',recursive=False)
            for one in length:
                df=df.append(pd.Series([date,'Pompeii','Home',shoe.string,color.string,model.string,model.next_sibling.next_sibling.string,one.string],index=df.columns), ignore_index=True)
        else:
            df=df.append(pd.Series([date,'Pompeii','Home',shoe.string,color.string,model.string,model.next_sibling.next_sibling.string,''],index=df.columns), ignore_index=True)

#Repetim tot el proces amb les dades corresponent als models de 'Dona' i juntem les dades al mateix dataframe
url2='https://www.pompeiibrand.com/collections/zapatillas-mujer'
page2=requests.get(url2)
soupwoman=BeautifulSoup(page2.content)

for collection in soupwoman.body.find_all('div',attrs={'class':'single-collection'}):
    shoe = collection.find('div',attrs={'class':'grid__item'}).h3
    for item in collection.find_all('a',attrs={'class':'grid-view-item__link'}):
        color=item.find('div',attrs={'class':'h4'}).span
        model=item.find('div',attrs={'class':'grid-view-item__meta'}).span
        sizes=item.find('div',attrs={'class':'sizes-wrap'})
        if sizes is not None:
            length=sizes.findChildren('span',recursive=False)
            for one in length:
                df=df.append(pd.Series([date,'Pompeii','Dona',shoe.string,color.string,model.string,model.next_sibling.next_sibling.string,one.string],index=df.columns), ignore_index=True)
        else:
            df=df.append(pd.Series([date,'Pompeii','Dona',shoe.string,color.string,model.string,model.next_sibling.next_sibling.string,''],index=df.columns), ignore_index=True)

#Escriu el fitxer a C:/Users/<Usuari actual>
date2=str(now.year)+'_'+str(now.month)+'_'+str(now.day)
df.to_csv('shoe-catalog-'+date2+'.csv',',', index = False)