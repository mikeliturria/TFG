from requests.sessions import Session
from bs4 import BeautifulSoup as soup


if __name__ == "__main__":
    # Creo una sesión para pasarle cookies. 
    # Si las cookies son diferentes en cada petición o no usas ninguna
    # puedes utilizar requests.get() y requests.post()
    s = Session()
    cookies = ['nombre=valor', 'nombre2=valor2']
    
    # Le paso las cookies a la session
    for item in cookies:
        cookie = item.split('=')
        name = cookie[0]
        value = cookie[1]
        s.cookies.set(name, value)
        
    # Se hace la petición
    r = s.get('https://elpais.com/')
    
    # le paso el html de la respuesta a BeautifulSoup
    page_soup = soup(r.text, features='html.parser')
    
    # Busco un h2 con su clase
    titulo = page_soup.find('h2', {'class': 'c_t c_t-sm'})
    # Tambien puedes usar para buscar elementos:
    #   page_soup.find_all()
    #   page_soup.select()
    
    print(titulo.text)
