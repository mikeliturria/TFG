from flask import Flask, request
from flask_cors import CORS, cross_origin

import concurrent.futures

from requests.sessions import Session
from bs4 import BeautifulSoup as soup
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/help')
def login():

    #NO SE HACE EL REPLACE BIEN
    url = "https:%2F%2Fwww.ehu.eus%2Fes%2Fhome"
    url.replace('%2F','/')

    print(url)
    return '<h1>Has pedido ayuda</h1>'

@app.route('/buscar/<url>')
def buscar(url):
    html = ""
    s = Session()
    #Vamos a sacar la web de access monitor
    url = "https:\%2F\%2Fwww.ehu.eus\%2Fes\%2Fhome"
    url = url.replace("\%2F","/")


    url = url.replace("/",'%2f')

    url = "https://accessmonitor.acessibilidade.gov.pt/results/"+url
    # print("URL fin: "+url)

    r = s.get(url)
    #Usar timeout?
    # r = s.get(url,  timeout=(3.05, 27))



    # le paso el html de la respuesta a BeautifulSoup
    #page_soup = soup(r.text, features='html.parser')
    page_soup = soup(r.text, features='html.parser')
    print(r.text)
    texto = r.text 
    html += "<xmp>"+texto+"</xmp>"

    
    # Busco un h2 con su clase
    #titulo = page_soup.find('h2 ', {'class': 'c_t c_t-sm'})
    # Tambien puedes usar para buscar elementos:
    #   page_soup.find_all()
    titulos = page_soup.find_all("h1")
    print("len; "+str(len(titulos)))

    #   page_soup.select()
    
    #html += "<h1>"+titulo.text+"</h1>"
    #html += "<h1>Nombre: "+name+"</h1>"
    return html

@app.route('/formaDos/')
def formaDos():

    #https://stackoverflow.com/questions/45448994/wait-page-to-load-before-getting-data-with-requests-get-in-python-3
    html_ = ""
    #s = Session()
    #Vamos a sacar la web de access monitor
    url = "https:\%2F\%2Fwww.ehu.eus\%2Fes\%2Fhome"
    url = url.replace("\%2F","/")


    url = url.replace("/",'%2f')

    url = "https://accessmonitor.acessibilidade.gov.pt/results/"+url

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    #Importante ponerle el lenguaje predefinido el inglés, sino sale en portugués
    options.add_argument("--lang=en");
    # executable_path param is not needed if you updated PATH
    browser = webdriver.Chrome(options=options, executable_path='./chromedriver.exe')


    try:
        browser.get(url)
        timeout_in_seconds = 50
        WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.CLASS_NAME, 'evaluation-table')))
        #Lo de abajo hace que se imprima la pagina
        html = browser.page_source
        s = soup(html, features="html.parser")

        #https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
        tabla = s.find('table', {'class': 'evaluation-table'})
        cabeza = tabla.find('tbody')

        score = s.find('div',{'class':'reading-block'})
        #El score puede venir bien para el resumen
        html_ += "<h1>Score: "+score.text+"</h1>"

        html_ +="<table><tr><th>TIPO</th><th>Nivel</th><th>Estandar</th><th>Error</th><th>Link</th></tr>"


        rows = cabeza.find_all('tr')

        for row in rows:
            html_ +="<tr>"
            cols = row.find_all('td')
            tipo_texto = cols[0].svg.title.text
            tipo = False
            if tipo_texto == 'monitor_icons_praticas_status_incorrect':
                tipo = True
                html_ += "<td><text style='color:RED'>ERROR</text></td>"
            elif tipo_texto == 'monitor_icons_praticas_status_review':
                tipo = True
                html_ += "<td><text style='color:#FFCD00'>WARNING</text></td>"
            elif tipo_texto == 'monitor_icons_praticas_status_correct':
                html_ += "<td><text style='color:GREEN'>CORRECTO</text></td>"
            
            #Si es un error o un warning habrá que hacer scraping
            link = ""
            texto_link = ""
            if tipo:
                link = cols[3].a.get('href')
                link = 'https://accessmonitor.acessibilidade.gov.pt'+link
                array_respuesta = get_content_of_link(link,browser,'AM')

                for i in array_respuesta:
                    i = i.replace('>','&gt;')
                    i = i.replace('<','&lt;')
                    texto_link += "<br><code>"+i+"</code>"
        
            html_ += "<td>"+cols[2].text+"</td>"
            divc = cols[1].find('div',{'class':'collapsible-content'})
            
            estandares = escribir_estandares(divc)

            html_ += "<td>"+estandares+"</td>"
            texto = divc.p.text

            html_ = escribir_texto(texto,html_)

            html_ += "<td>"+texto_link+"</td>"

            html_ +="</tr>"

        html_ +="</table>"


    except TimeoutException:
        print("I give up...")
    finally:
        browser.quit()
        return html_

    return html_


def escribir_texto(texto, html_):
    txt_nuevo=""            
    pos = texto.find("<")
    #pos = texto.find("&lt;")
    entro = False
    while pos != -1:
        entro = True
        txt_nuevo += texto[:pos]+"<code>&lt;"
        texto = texto[pos+1:]
        pos = texto.find(">")
        #pos = texto.find("&gt;")
        txt_nuevo += texto[:pos]+"&gt;</code>"
        texto = texto[pos+1:]
        pos = texto.find("<")
        #pos = texto.find("&lt;")

    if entro:
        txt_nuevo += texto
        html_ += "<td>"+txt_nuevo+"</td>"
    else:
        html_ += "<td>"+texto+"</td>"
    return html_

def escribir_estandares(divc):
    estandars = divc.find_all('li')
    estandares = ""
    coma = False
    for es in estandars:
        if not coma:
            coma=True 
            estandares += es.text[17:24]
        else:
            estandares +=", "+es.text[17:24]

    return estandares

def get_content_of_link(url,browser,tipo):
    array_respuesta= []
    #Ojo no se tiene en cuenta de que pueda fallar (no hay try except finally) porque no se puede hacer el browser quit
    if tipo =='AM' and url.startswith('https://accessmonitor.acessibilidade.gov.pt'):
        #Uno de los links va a w3c
        browser.get(url)
        timeout_in_seconds = 50
        WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.ID, 'list_tab')))
        #Lo de abajo hace que se imprima la pagina
        html = browser.page_source
        res = soup(html, features="html.parser")

        div = res.find('div',{'id':'list_tab'})

        ol = div.ol

        lis = ol.find_all('li')

        for li in lis:
            table = li.table 
            trs = table.find_all('tr')
            td = trs[1].td
            codigo = td.code.text
            array_respuesta.append(codigo)
    else:
        array_respuesta.append(url)

    return array_respuesta

@app.route('/getJSON/', methods=['POST'])
@cross_origin()
def create_JSON():
    received_json = request.get_json()
    url = received_json['url']
    print("U: "+url)
    #url = "https:\%2F\%2Fwww.ehu.eus\%2Fes\%2Fhome"
    #url = url.replace("\%2F","/")

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
      f1 = ex.submit(JSON_access_monitor, url)
      f2 = ex.submit(achecker, url)
      # Wait for results
      informe = f1.result()
      informe_2 = f2.result()

    #informe = JSON_access_monitor(url)
    #informe_2 = achecker(url)
    #informe = informe1()
    #informe_2 = informe2()
    informe_final = merge_reports(informe, informe_2)
    informe_final = fomat_informe(url,informe_final)
    return informe_final


def JSON_access_monitor(url):
    s = Session()
    #Vamos a sacar la web de access monitor
    url = url.replace("/",'%2f')

    url = "https://accessmonitor.acessibilidade.gov.pt/results/"+url

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    #Importante ponerle el lenguaje predefinido el inglés, sino sale en portugués
    options.add_argument("--lang=en");
    # executable_path param is not needed if you updated PATH
    browser = webdriver.Chrome(options=options, executable_path='./chromedriver.exe')

    informe = {
        'Tester_Name' : 'Access_Monitor'
    }

    try:
        browser.get(url)
        timeout_in_seconds = 50
        WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.CLASS_NAME, 'evaluation-table')))
        #Lo de abajo hace que se imprima la pagina
        html = browser.page_source
        s = soup(html, features="html.parser")

        #https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
        tabla = s.find('table', {'class': 'evaluation-table'})
        cabeza = tabla.find('tbody')

        score = s.find('div',{'class':'reading-block'})
        #El score puede venir bien para el resumen
        informe['RESULTADO']=score.text

        rows = cabeza.find_all('tr')

        '''
        Editar todo lo de abajo para que se haga de la siguiente forma:
        1-Sacamos los estandares
        2-Analizamos los resultados creando un mini array: ["ADVERTENCIA", "TextoError","CodigoError"]
        3- Bucle, por cada estandar, buscamos su equivalente en el diccionario recien creado y luego escribimos algo tal que asi:

        dic = {"WCAG21:non-text-content": {}, "WCAG21:audio-only-and-video-only-prerecorded": {"error": "True", "texto": "textp"}}

    for key,v in dic.items():
        print("Key: "+key)
        print("Values:")
        for vk,val in v.items():
            print(vk+": "+val)
    print("Hola")
        '''
        informe_casos = {}
        for row in rows:
            cols = row.find_all('td')
            divc = cols[1].find('div',{'class':'collapsible-content'})
            nivel = cols[2].text
            nivel = nivel.replace(' ','')
            if str(nivel) == 'A' or str(nivel) =='AA':
                estandares = get_estandares_array(divc)
                array_prueba = []

                cols = row.find_all('td')
                tipo_texto = cols[0].svg.title.text
                tipo = False
                texto_final = ""
                if tipo_texto == 'monitor_icons_praticas_status_incorrect':
                    tipo = True
                    array_prueba.append("Failed")
                    texto_final += "The next ERROR was found: \n\n"
                elif tipo_texto == 'monitor_icons_praticas_status_review':
                    tipo = True
                    array_prueba.append("Cannot Tell")
                    texto_final += "The next WARNING was found: \n\n"
                elif tipo_texto == 'monitor_icons_praticas_status_correct':
                    array_prueba.append("Passed")
                    texto_final += "The next CORRECTION CHECK was found: \n\n"
                
                #Si es un error o un warning habrá que hacer scraping
                link = ""
                texto_link = ""
                if tipo:
                    link = cols[3].a.get('href')
                    link = 'https://accessmonitor.acessibilidade.gov.pt'+link
                    array_respuesta = get_content_of_link(link,browser,'AM')

                    for i in array_respuesta:
                        i=i.replace('\n','')
                        i=i.replace('\t','')
                        texto_link += i+"\n\n"

                texto_final += divc.p.text

                if tipo:
                    texto_final += "On the code: \n\n"
                    texto_final += texto_link


                #Metemos el texto con los links
                array_prueba.append(texto_final)

                #Una vez el array lleno, llenamos los estandares con los valores.
                codes = nombres_por_codigos()
                for estandar in estandares:
                    estandar = estandar.replace(' ','')
                    if estandar in codes:
                        nombre_wag = codes[estandar]
                        if nombre_wag in informe_casos:

                            resultado_Previo = informe_casos[nombre_wag]['Resultado']
                            texto_Previo = informe_casos[nombre_wag]['Texto']
                            resultado_Actual = array_prueba[0]
                            texto_Actual = array_prueba[1]

                            if resultado_Previo =='Failed'or resultado_Actual == 'Failed':
                                informe_casos[nombre_wag]['Resultado'] = 'Failed'
                            elif resultado_Previo =='Cannot Tell'or resultado_Actual == 'Cannot Tell':
                                informe_casos[nombre_wag]['Resultado'] = 'Cannot Tell'
                            else:
                                informe_casos[nombre_wag]['Resultado'] = 'Passed'
    

                            texto_r = texto_Previo +"---------------------------------------- \n\n "+texto_Actual
                            informe_casos[nombre_wag]['Texto'] = texto_r

                        else:
                            informe_casos[nombre_wag] = {
                                'Resultado': array_prueba[0],
                                'Texto' : array_prueba[1]
                            }
    except TimeoutException:
        print("I give up...")
    finally:
        browser.quit()
        informe['Cases'] = informe_casos
        print("AM hecho")
        return informe


    return informe


def nombres_por_codigos():
    cod = {
    '1.1.1':'WCAG21:non-text-content',
    '1.2.1':'WCAG21:audio-only-and-video-only-prerecorded',
    '1.2.2':'WCAG21:captions-prerecorded',
    '1.2.3':'WCAG21:audio-description-or-media-alternative-prerecorded',
    '1.2.4':'WCAG21:captions-live',
    '1.2.5':'WCAG21:audio-description-prerecorded',
    '1.3.1':'WCAG21:info-and-relationships',
    '1.3.2':'WCAG21:meaningful-sequence',
    '1.3.3':'WCAG21:sensory-characteristics',
    '1.3.4':'WCAG21:orientation',
    '1.3.5':'WCAG21:identify-input-purpose',
    '1.4.1':'WCAG21:use-of-color',
    '1.4.2':'WCAG21:audio-control',
    '1.4.3':'WCAG21:contrast-minimum',
    '1.4.4':'WCAG21:resize-text',
    '1.4.5':'WCAG21:images-of-text',
    '1.4.10':'WCAG21:reflow',
    '1.4.11':'WCAG21:non-text-contrast',
    '1.4.12':'WCAG21:text-spacing',
    '1.4.13':'WCAG21:content-on-hover-or-focus',
    '2.1.1':'WCAG21:keyboard',
    '2.1.2':'WCAG21:no-keyboard-trap',
    '2.1.4':'WCAG21:character-key-shortcuts',
    '2.2.1':'WCAG21:timing-adjustable',
    '2.2.2':'WCAG21:pause-stop-hide',
    '2.3.1':'WCAG21:three-flashes-or-below-threshold',
    '2.4.1':'WCAG21:bypass-blocks',
    '2.4.2':'WCAG21:page-titled',
    '2.4.3':'WCAG21:focus-order',
    '2.4.4':'WCAG21:link-purpose-in-context',
    '2.4.5':'WCAG21:multiple-ways',
    '2.4.6':'WCAG21:headings-and-labels',
    '2.4.7':'WCAG21:focus-visible',
    '2.5.1':'WCAG21:pointer-gestures',
    '2.5.2':'WCAG21:pointer-cancellation',
    '2.5.3':'WCAG21:label-in-name',
    '2.5.4':'WCAG21:motion-actuation',
    '3.1.1':'WCAG21:language-of-page',
    '3.1.2':'WCAG21:language-of-parts',
    '3.2.1':'WCAG21:on-focus',
    '3.2.2':'WCAG21:on-input',
    '3.2.3':'WCAG21:consistent-navigation',
    '3.2.4':'WCAG21:consistent-identification',
    '3.3.1':'WCAG21:error-identification',
    '3.3.2':'WCAG21:labels-or-instructions',
    '3.3.3':'WCAG21:error-suggestion',
    '3.4.3':'WCAG21:error-prevention-legal-financial-data',
    '4.1.1':'WCAG21:parsing',
    '4.1.2':'WCAG21:name-role-value',
    '4.1.3':'WCAG21:status-messages'
    }
    return cod


def get_estandares_array(divc):
    estandars = divc.find_all('li')
    estandares = []
    for es in estandars:
        estandares.append(es.text[17:24])

    return estandares


@app.route('/formaTres/')
def wave_html():

    #https://stackoverflow.com/questions/45448994/wait-page-to-load-before-getting-data-with-requests-get-in-python-3
    html_ = ""
    s = Session()
    #Vamos a sacar la web de access monitor
    url = "https:\%2F\%2Fwww.ehu.eus\%2Fes\%2Fhome"
    url = url.replace("\%2F","/")


    #url = url.replace("/",'%2f')

    url = "https://wave.webaim.org/report#/"+url

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    #Importante ponerle el lenguaje predefinido el inglés, sino sale en portugués
    options.add_argument("--lang=en")
    #Ojo, ponemos el CORS porque sino bloquea
    options.add_argument("--allow-cors")
    options.add_argument("--Access-Control-Allow-Origin=*")
    # executable_path param is not needed if you updated PATH
    browser = webdriver.Chrome(options=options, executable_path='./chromedriver.exe')


    try:
        browser.get(url)
        timeout_in_seconds = 50
        #WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.ID, 'report_container')))
        #WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.XPATH,"//body[contains(@style, 'opacity: 1;')]")))
        WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.XPATH,"//*[@id='wave5_iconbox'][contains(@style, 'opacity: 0;')]")))
        #webdriver.wait().until(ExpectedConditions.presenceOfElementLocated(By.xpath("//*[@id='some_input'][contains(@style, 'display: block')]")));

        #ahora habría que probar a hacer browser.click por cada error etc

        #Lo de abajo hace que se imprima la pagina
        html = browser.page_source
        s = soup(html, features="html.parser")


        boton_details = browser.find_element(By.ID, "tab-details")
        boton_details.click()

        html = browser.page_source
        s = soup(html, features="html.parser")

        #Obtenemos la lista de los errores normales, de contraste y warnings
        div = s.find('div',{'id':'iconlist'})
        #div = s.find('div',{'id':'iconlist'})
        divs = div.find_all('div',{'class':'icon_group'})

        html, browser = get_content_wave(divs,browser)

    except TimeoutException:
        print("I give up...")
    finally:
        browser.quit()
        return html


def get_content_wave(divs,browser):
    #Desclicamos todos los campos para que los logos iconos que se muestren sean en cada momento los que queremos
    browser = desactivar_botones(divs,browser)
    html = ''
    html += "<table><tr><th>TIPO</th><th>Mensaje</th><th>Cantidad</th><th>Iconos</th><th>Estandar</th></tr>"

    for d in divs:
        tipo = d.h3['id']
        if tipo =='group_error':
            tipo_text = "<td>ERROR</td>"
            #activamos el boton
            boton_quitar_errores = browser.find_element(By.ID, "toggle_group_error")
            boton_quitar_errores.click() 
            html1, browser = get_info_elementos_wave(browser,d, tipo_text)
            html += html1
            boton_quitar_errores.click()
        elif tipo == 'group_contrast':
            tipo_text ="<td>Contrast ERROR</td>"
            boton_quitar_errores_contraste = browser.find_element(By.ID, "toggle_group_contrast")
            boton_quitar_errores_contraste.click()
            html1, browser = get_info_elementos_wave(browser,d, tipo_text)
            html += html1
            boton_quitar_errores_contraste.click()
        elif tipo=='group_alert':
            tipo_text ="<td>Warning</td>"
            boton_quitar_alertas = browser.find_element(By.ID, "toggle_group_alert")
            boton_quitar_alertas.click()
            html1, browser = get_info_elementos_wave(browser,d, tipo_text)
            html += html1
            boton_quitar_alertas.click()
        elif tipo=='group_feature':
            tipo_text ="<td>Correciones</td>"
            boton_quitar_correciones = browser.find_element(By.ID, "toggle_group_feature")
            boton_quitar_correciones.click()
            html1, browser = get_info_elementos_wave(browser,d, tipo_text)
            html += html1
            boton_quitar_correciones.click()
    return html, browser



def get_info_elementos_wave(browser,d, tipo_text):
    html = ''
    lis = d.ul.find_all('li',{'class':'icon_type'})
    for l in lis:
        html +="<tr>"
        html +=tipo_text

        fallo = l.h4.label.text
        pos = fallo.find('X')+2
        fallo = fallo[pos:]
        html += "<td>"+fallo+"</td>"
        #Ya tenemos los titulos, ya solo queda que por cada titulo se haga un click
        lis_internos = l.ul.find_all('li')
        cuantos = len(lis_internos)-1
        html += "<td>"+str(cuantos)+"</td>"
        html += "<td><table border='1'>"
        for li_int in lis_internos:
            src = li_int.img['src']
            xpath = "*//img[@src='"+src+"']"

            '''
            Hay que intentar por aquí
            '''


            elementos_de_fallo = browser.find_elements(By.XPATH,xpath )
            #hrml_SOURCE="SOURCE"+browser.page_source
            if src != "/img/icon_reference.svg":
                html+= "<tr><td>"+src+"</td>"
            html += "<td>"
            #print(len(elementos_de_fallo))
            #html += "<pre><code>"+hrml_SOURCE+"</code></pre>"

            #for elemento_de_fallo in elementos_de_fallo:
            #    html += "<pre><code>"+elemento_de_fallo.get_attribute('innerHTML')+"</code></pre>"
            html += "</td></tr>"
        html += "</table></td>"

        #Obtenemos estandar
        id_del_ul = l.ul.get('id')
        #html += "<td>"+str(id_del_ul)+"</td>"
        cuantos +=1
        es = browser.find_element(By.XPATH,"//*[@id='"+id_del_ul+"']/li["+str(cuantos)+"]/a" )
        es.click()
        tabla_ref = browser.find_element(By.ID, 'tab_docs_container')
        #html += "<td>"+str(tabla_ref.get_attribute('innerHTML'))+"</td>"
        s_ref = soup(tabla_ref.get_attribute('innerHTML'),features="html.parser")
        ul = s_ref.find('ul',{'id':'tab_docs_guidelines'})
        lis_estandares = ul.find_all('li')
        estandares = ''
        for l_s in lis_estandares:
            #OJO!!! No se tiene en cuenta que los estandares sean de A o de AAA...
            texto = l_s.a.text
            pos = texto.find(' ')
            texto = texto[:pos]
            estandares += texto+", "
        if len(lis_estandares) == 0:
            estandares = "NONE"
        
        html += "<td>"+estandares+"</td>"

        atras = browser.find_element(By.XPATH, "//*[@id='tab-details']")
        atras.click()

        html += "</tr>"

    return html,browser


def desactivar_botones(d,browser):
    tipo = []
    for d_ in d:
        tipo.append(d_.h3['id'])

    tipo = list(dict.fromkeys(tipo))


    for t in tipo:
        if t == 'group_error':
            boton_quitar_errores = browser.find_element(By.ID, "toggle_group_error")
            boton_quitar_errores.click() 
        elif t == 'group_contrast':
            boton_quitar_errores_contraste = browser.find_element(By.ID, "toggle_group_contrast")
            boton_quitar_errores_contraste.click()
        elif t == 'group_feature':
            boton_quitar_correciones = browser.find_element(By.ID, "toggle_group_feature")
            boton_quitar_correciones.click()
        elif t == 'group_alert':
            boton_quitar_alertas = browser.find_element(By.ID, "toggle_group_alert")
            boton_quitar_alertas.click()
        elif t == 'group_structure':
            boton_quitar_aria = browser.find_element(By.ID, "toggle_group_aria")
            boton_quitar_aria.click()
        elif t == 'group_aria':
            boton_quitar_str = browser.find_element(By.ID, "toggle_group_aria")
            boton_quitar_str.click()
    return browser

@app.route('/achecker/')
def achecker(url):
    ac = "https://achecker.achecks.ca/checker/index.php"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    #Importante ponerle el lenguaje predefinido el inglés, sino sale en portugués
    options.add_argument("--lang=en");
    # executable_path param is not needed if you updated PATH
    browser = webdriver.Chrome(options=options, executable_path='./chromedriver.exe')


    try:
        browser.get(ac)
        #timeout_in_seconds = 50
        #WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.CLASS_NAME, 'evaluation-table')))
        #Lo de abajo hace que se imprima la pagina
        html = browser.page_source
        #s = soup(html, features="html.parser")

        campo_de_texto = browser.find_element(By.ID, "checkuri")
        campo_de_texto.send_keys(url)
        boton_submit = browser.find_element(By.ID, "validate_uri")
        boton_submit.click()
        html = browser.page_source

        informe = get_contenido_achecker(browser)


    except TimeoutException:
        print("I give up...")
    finally:
        browser.quit()
        print("AC hecho")
        return informe

def get_contenido_achecker(browser):
    informe = {
        'Tester_Name' : 'Achecker'
    }

    html_s = browser.page_source
    s = soup(html_s, features="html.parser")

    #Errores conocidos
    div_AC_ERRORS = s.find('div',{'id':'AC_errors'}) 
    h4_AC_ERRORS = div_AC_ERRORS.find_all('h4')
    one_check_AC_ERRORS = div_AC_ERRORS.find_all('div',{'class':'gd_one_check'})

    codes = nombres_por_codigos()
    inf_casos = {}
    for i in range(0,len(h4_AC_ERRORS)):
        text_criteria=h4_AC_ERRORS[i].text[17:]
        pos = text_criteria.find(' ')
        text_criteria = text_criteria[:pos]
        one_check = one_check_AC_ERRORS[i]
        problema = one_check.span.a.text
        solucion = one_check.div.text
        tabla_lineas = one_check.table.tbody
        trs = tabla_lineas.find_all('tr')
        errores_y_lineas = []
        for tr in trs:
            td = tr.td 
            linea_error= td.em
            codigo = td.pre.code
            errores_y_lineas.append({
                'linea':str(linea_error),
                'codigo':str(codigo)
                })
        texto_Actual = 'The next ERROR was found: "'+problema+'". You can solve it with: "'+solucion+'". The error was in the following line(s): \n\n "'
        for er in errores_y_lineas:
            texto_Actual+= 'LINE '+er['linea']+': "'+er['codigo']+'"\n\n'
        if text_criteria in codes:
            nombre_wag = codes[text_criteria]
            if nombre_wag in inf_casos:

                texto_Previo = inf_casos[nombre_wag]['Texto']
                inf_casos[nombre_wag]['Resultado'] = 'Failed'


                texto_r = texto_Previo +"---------------------------------------- \n\n "+texto_Actual
                inf_casos[nombre_wag]['Texto'] = texto_r

            else:
                inf_casos[nombre_wag] = {
                    'Resultado':'Failed',
                    'Texto' : texto_Actual
                }



    #Avisos (likely errors)
    div_AC_likely_problems = s.find('div',{'id':'AC_likely_problems'}) 
    h4_AC_likely_problems = div_AC_likely_problems.find_all('h4')
    one_check_AC_likely_problems = div_AC_likely_problems.find_all('div',{'class':'gd_one_check'})

    for i in range(0,len(h4_AC_likely_problems)):
        text_criteria=h4_AC_likely_problems[i].text[17:]
        pos = text_criteria.find(' ')
        text_criteria = text_criteria[:pos]
        one_check = one_check_AC_likely_problems[i]
        problema = one_check.span.a.text
        tabla_lineas = one_check.table.tbody
        trs = tabla_lineas.find_all('tr')
        errores_y_lineas = []
        for tr in trs:
            td = tr.td 
            linea_error= td.em
            codigo = td.pre.code
            errores_y_lineas.append({
                'linea':str(linea_error),
                'codigo':str(codigo)
                })

        texto_Actual = 'The next WARNING was found: "'+problema+'". The warning was in the following line(s): \n\n "'
        for er in errores_y_lineas:
            texto_Actual+= 'LINE '+er['linea']+': "'+er['codigo']+'".\n\n'
        if text_criteria in codes:
            nombre_wag = codes[text_criteria]
            if nombre_wag in inf_casos:
                resultado_Previo = inf_casos[nombre_wag]['Resultado']
                texto_Previo = inf_casos[nombre_wag]['Texto']
                resultado_Actual = 'Failed'

                if resultado_Previo =='Failed':
                    inf_casos[nombre_wag]['Resultado'] = 'Failed'
                else:
                    inf_casos[nombre_wag]['Resultado'] = 'Cannot Tell'


                texto_r = texto_Previo +"---------------------------------------- \n\n "+texto_Actual
                inf_casos[nombre_wag]['Texto'] = texto_r

            else:
                inf_casos[nombre_wag] = {
                    'Resultado':'Cannot Tell',
                    'Texto' : texto_Actual
                }

    #Checkear (potential problems)
    div_AC_potential_problems = s.find('div',{'id':'AC_potential_problems'}) 
    h4_AC_potential_problems = div_AC_potential_problems.find_all('h4')
    one_check_AC_potential_problems = div_AC_potential_problems.find_all('div',{'class':'gd_one_check'})

    for i in range(0,len(h4_AC_potential_problems)):
        text_criteria=h4_AC_potential_problems[i].text[17:]
        pos = text_criteria.find(' ')
        text_criteria = text_criteria[:pos]
        one_check = one_check_AC_potential_problems[i]
        problema = one_check.span.a.text
        tabla_lineas = one_check.table.tbody
        trs = tabla_lineas.find_all('tr')
        errores_y_lineas = []
        for tr in trs:
            td = tr.td 
            linea_error= td.em
            codigo = td.pre.code
            errores_y_lineas.append({
                'linea':str(linea_error),
                'codigo':str(codigo)
                })

        texto_Actual = 'A POTENTIAL PROBLEM was found: "'+problema+'". The potential problem was in the following line(s): \n\n "'
        for er in errores_y_lineas:
            texto_Actual+= 'LINE '+er['linea']+': "'+er['codigo']+'".\n\n'
        if text_criteria in codes:
            nombre_wag = codes[text_criteria]
            if nombre_wag in inf_casos:

                resultado_Previo = inf_casos[nombre_wag]['Resultado']
                texto_Previo = inf_casos[nombre_wag]['Texto']

                if resultado_Previo =='Failed':
                    inf_casos[nombre_wag]['Resultado'] = 'Failed'
                #elif resultado_Previo =='Cannot Tell':
                else:
                    inf_casos[nombre_wag]['Resultado'] = 'Cannot Tell'
                #else:
                #    inf_casos[nombre_wag]['Resultado'] = 'Not checked'


                texto_r = texto_Previo +"---------------------------------------- \n\n "+texto_Actual
                inf_casos[nombre_wag]['Texto'] = texto_r

            else:
                inf_casos[nombre_wag] = {
                    'Resultado':'Cannot Tell',
                    'Texto' : texto_Actual
                }

            informe['Cases'] = inf_casos


    return informe



def merge_reports(informe1, informe2):
    autor1 = '@'+informe1['Tester_Name']
    autor2 = '@'+informe2['Tester_Name']
    tester_name = str(informe1['Tester_Name'])+' & '+str(informe2['Tester_Name'])

    informe_final = {
           'Tester_Name': tester_name,
           'Summary': '@Access_monitor mark:'+informe1['RESULTADO']
    }

    #Primero añadimos los datos del informe 1
    for key,value in informe1['Cases'].items():
        informe_final[key] = {
            'Resultado' : value['Resultado'],
            'Texto' : '*************'+autor1+'************* \n\n'+value['Texto']+'\n\n ************************** \n\n'
        }

    #Ahora los del informe 2
    for key,value in informe2['Cases'].items():
        #Comprobamos si ya está en el informe
        if key in informe_final:
            resultado_Previo = informe_final[key]['Resultado']
            texto_Previo = informe_final[key]['Texto']
            resultado_Actual = value['Resultado']
            texto_Actual = value['Texto']

            if resultado_Previo =='Failed'or resultado_Actual == 'Failed':
                informe_final[key]['Resultado'] = 'Failed'
            elif resultado_Previo =='Cannot Tell'or resultado_Actual == 'Cannot Tell':
                informe_final[key]['Resultado'] = 'Cannot Tell'
            else:
                informe_final[key]['Resultado'] = 'Passed'


            texto_r = texto_Previo +'*************'+autor2+'************* \n\n'+value['Texto']+'\n\n ************************** \n\n'
            informe_final[key]['Texto'] = texto_r

        else:
            informe_final[key] = {
                'Resultado' : value['Resultado'],
                'Texto' : '*************'+autor2+'************* \n\n'+value['Texto']+'\n\n ************************** \n\n'
            } 
    return informe_final

def fomat_informe(url,informe):
    description = url
    pos = url.find('.')
    url = url[pos+1:]
    pos = url.find('.')
    url = url[:pos]
    informe_limpio = crear_JSON_limpio()
    autores = informe['Tester_Name']
    resultado = informe['Summary']

    informe_limpio['reportFindings']['commissioner'] = 'AUTHOMATIC'
    informe_limpio['reportFindings']['evaluator'] = autores
    informe_limpio['defineScope']['scope'] = {
            "description": str(description),
            "title": str(url)
        }

    longitud = len(informe_limpio['auditSample'])

    #Queda por meter description y fecha
    for i in range(0,longitud):
        tipo = informe_limpio['auditSample'][i]['test']['id']
        if tipo in informe:
            obj = informe[tipo]
            if obj['Resultado'] =='Failed':
                informe_limpio['auditSample'][i]['result']['outcome'] ={
                    "id": "earl:failed",
                    "type": ["OutcomeValue", "Fail"],
                    "title":"Failed"
                }
            elif obj['Resultado'] == 'Cannot Tell':
                informe_limpio['auditSample'][i]['result']['outcome'] = {
                    "id": "earl:cantTell",
                    "type": ["OutcomeValue", "CannotTell"],
                    "title": "Cannot tell"
                }

            elif obj['Resultado'] == 'Not checked':
                informe_limpio['auditSample'][i]['result']['outcome'] = {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"],
                    "title": "Not checked"
                }
            else:
                informe_limpio['auditSample'][i]['result']['outcome'] = {
                    "id": "earl:passed",
                    "type": ["OutcomeValue", "Pass"],
                    "title": "Passed"
                }
            informe_limpio['auditSample'][i]['result']['description'] = obj['Texto']
    return informe_limpio


def crear_JSON_limpio():
    now = datetime.now()
    time = str(now.strftime("%a %b %d %Y"))
    json = {
        "@context": {
            "reporter": "http://github.com/w3c/wai-wcag-em-report-tool/",
            "wcagem": "http://www.w3.org/TR/WCAG-EM/#",
            "Evaluation": "wcagem:procedure",
            "defineScope": "wcagem:step1",
            "scope": "wcagem:step1a",
            "step1b": {
                "@id": "wcagem:step1b",
                "@type": "@id"
            },
            "conformanceTarget": "step1b",
            "accessibilitySupportBaseline": "wcagem:step1c",
            "additionalEvaluationRequirements": "wcagem:step1d",
            "exploreTarget": "wcagem:step2",
            "essentialFunctionality": "wcagem:step2b",
            "pageTypeVariety": "wcagem:step2c",
            "technologiesReliedUpon": "wcagem:step2d",
            "selectSample": "wcagem:step3",
            "structuredSample": "wcagem:step3a",
            "randomSample": "wcagem:step3b",
            "Website": "wcagem:website",
            "Webpage": "wcagem:webpage",
            "auditSample": "wcagem:step4",
            "reportFindings": "wcagem:step5",
            "documentSteps": "wcagem:step5a",
            "commissioner": "wcagem:commissioner",
            "evaluator": "wcagem:evaluator",
            "evaluationSpecifics": "wcagem:step5b",
            "WCAG": "http://www.w3.org/TR/WCAG/#",
            "WCAG20": "http://www.w3.org/TR/WCAG20/#",
            "WCAG21": "http://www.w3.org/TR/WCAG21/#",
            "WAI": "http://www.w3.org/WAI/",
            "A": "WAI:WCAG2A-Conformance",
            "AA": "WAI:WCAG2AA-Conformance",
            "AAA": "WAI:WCAG2AAA-Conformance",
            "wcagVersion": "WAI:standards-guidelines/wcag/#versions",
            "reportToolVersion": "wcagem:reportToolVersion",
            "earl": "http://www.w3.org/ns/earl#",
            "Assertion": "earl:Assertion",
            "TestMode": "earl:TestMode",
            "TestCriterion": "earl:TestCriterion",
            "TestCase": "earl:TestCase",
            "TestRequirement": "earl:TestRequirement",
            "TestSubject": "earl:TestSubject",
            "TestResult": "earl:TestResult",
            "OutcomeValue": "earl:OutcomeValue",
            "Pass": "earl:Pass",
            "Fail": "earl:Fail",
            "CannotTell": "earl:CannotTell",
            "NotApplicable": "earl:NotApplicable",
            "NotTested": "earl:NotTested",
            "assertedBy": "earl:assertedBy",
            "mode": "earl:mode",
            "result": "earl:result",
            "subject": "earl:subject",
            "test": "earl:test",
            "outcome": "earl:outcome",
            "dcterms": "http://purl.org/dc/terms/",
            "title": "dcterms:title",
            "description": "dcterms:description",
            "summary": "dcterms:summary",
            "date": "dcterms:date",
            "hasPart": "dcterms:hasPart",
            "isPartOf": "dcterms:isPartOf",
            "id": "@id",
            "type": "@type",
            "language": "@language"
        },
        "language": "en",
        "type": "Evaluation",
        "reportToolVersion": "3.0.3",
        "defineScope": {
            "id": "_:defineScope",
            "scope": {
                "description": "",
                "title": ""
            },
            "conformanceTarget": "AA",
            "accessibilitySupportBaseline": "",
            "additionalEvaluationRequirements": "",
            "wcagVersion": "2.1"
        },
        "exploreTarget": {
            "id": "_:exploreTarget",
            "essentialFunctionality": "",
            "pageTypeVariety": "",
            "technologiesReliedUpon": []
        },
        "selectSample": {
            "id": "_:selectSample",
            "structuredSample": [],
            "randomSample": []
        },
        "auditSample": [{
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.699Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.699Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:non-text-content",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.700Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.700Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:audio-only-and-video-only-prerecorded",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.700Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.700Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:captions-prerecorded",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.700Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.700Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:audio-description-or-media-alternative-prerecorded",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.701Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.701Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:captions-live",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.701Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.701Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:audio-description-prerecorded",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.701Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.701Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:info-and-relationships",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.701Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.701Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:meaningful-sequence",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.701Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.701Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:sensory-characteristics",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.701Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.701Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:orientation",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.701Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:identify-input-purpose",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:use-of-color",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:audio-control",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:contrast-minimum",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:resize-text",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:images-of-text",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.540Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:reflow",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:non-text-contrast",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:text-spacing",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:content-on-hover-or-focus",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:keyboard",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:no-keyboard-trap",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:character-key-shortcuts",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.702Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:timing-adjustable",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.702Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:pause-stop-hide",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.703Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:three-flashes-or-below-threshold",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.703Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:bypass-blocks",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.703Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:page-titled",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.703Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:focus-order",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.703Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:link-purpose-in-context",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.703Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:multiple-ways",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.703Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:headings-and-labels",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.703Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:focus-visible",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.703Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:pointer-gestures",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.703Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:pointer-cancellation",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.703Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:label-in-name",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.703Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.703Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:motion-actuation",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.704Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.704Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:language-of-page",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.704Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.704Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:language-of-parts",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.704Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.704Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:on-focus",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.704Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.704Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:on-input",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.704Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.704Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:consistent-navigation",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.704Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.704Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:consistent-identification",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.541Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.704Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.704Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:error-identification",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.542Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.704Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.704Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:labels-or-instructions",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.542Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.704Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.704Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:error-suggestion",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.542Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.704Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.704Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:error-prevention-legal-financial-data",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.542Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.704Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.704Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:parsing",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.542Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.705Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.705Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:name-role-value",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.542Z"
            }
        }, {
            "type": "Assertion",
            "date": "2022-03-01T18:51:57.705Z",
            "mode": {
                "type": "TestMode",
                "@value": "earl:manual"
            },
            "result": {
                "type": "TestResult",
                "date": "2022-03-01T18:51:57.705Z",
                "description": "",
                "outcome": {
                    "id": "earl:untested",
                    "type": ["OutcomeValue", "NotTested"]
                }
            },
            "subject": {
                "id": "_:subject_1",
                "type": ["TestSubject", "Website"],
                "date": "2022-03-01T18:51:52.539Z",
                "description": "",
                "title": ""
            },
            "test": {
                "id": "WCAG21:status-messages",
                "type": ["TestCriterion", "TestRequirement"],
                "date": "2022-03-01T18:51:52.542Z"
            }
        }],
        "reportFindings": {
            "date": {
                "type": "http://www.w3.org/TR/NOTE-datetime",
                "@value": time
            },
            "summary": "",
            "title": "",
            "commissioner": "",
            "evaluator": "",
            "documentSteps": [{
                "id": "_:about"
            }, {
                "id": "_:defineScope"
            }, {
                "id": "_:exploreTarget"
            }, {
                "id": "_:selectSample"
            }],
            "evaluationSpecifics": ""
        }
    }
    return json

@app.route('/informe1/')
def informe1():
    informe = {
      "Cases": {
        "WCAG21:bypass-blocks": {
          "Resultado": "Cannot Tell", 
          "Texto": "The next WARNING was found: \n\nMake available at\u00a0the top of the webpage a link that allows skipping\u00a0directly to the main content of the webpage. This link facilitates the navigation to many users, namely those who use scanning selection software. These users use vision to read information so the links must be always visible ou become visible when receiving the focus.On the code: \n\n<a href=\"#main-content\">Saltar al contenido</a>\n\n---------------------------------------- \n\n The next WARNING was found: \n\nCheck if the links that I found\u00a0provide the most suitable\u00a0skips to the\u00a0content; if\u00a0 they are\u00a0 always visible or if become visible when receiving focus by keyboard.On the code: \n\n<a href=\"#main-content\">Saltar al contenido</a>\n\n<div class=\"upv-ehu-3-cols columns-3 container\" id=\"main-content\" role=\"main\">                                            Inicio      Inicio        Men\u00fa       Abrir/cerrar men\u00fa del sitio                                Perfiles Mostrar/ocultar subp\u00e1ginas                                                    Alumnado                                                                Futuro alumnado                                                                EHUalumni                                                                Profesorado                                                                Personal de Administraci\u00f3n y Servicios                                                                Empresas                                      Estudios Mostrar/ocultar subp\u00e1ginas                                                    EHU edonondik                                                                Estudios de grado                                                                Estudios de posgrado                                                                eCampus: campus virtual                                      Estructura UPV/EHU Mostrar/ocultar subp\u00e1ginas                                                    Informaci\u00f3n institucional                                                                \u00c1rea de la Rectora                                                                Equipo de Gobierno                                                                Consejo de Gobierno                                                                Aldezle                                                                Centros                                                                Departamentos                                                                Institutos                                      \u00c1reas tem\u00e1ticas Mostrar/ocultar subp\u00e1ginas                                                    EHUkultura                                                                Becas y Ayudas                                                                Direcci\u00f3n para la Igualdad                                                                Euskera                                                                Pluriling\u00fcismo                                                                Sostenibilidad                                                                Proyecci\u00f3n universitaria                                                                Relaciones internacionales                                                                Transparencia                                                                EHUkirola                                      Servicios Mostrar/ocultar subp\u00e1ginas                                                    Biblioteca                                                                Editorial                                                                Oficina de Comunicaci\u00f3n                                                                Perfil del contratante                                             \u00a1S\u00edguenos!TwitterFacebookInstagramLinkedinYoutubeVimeo     if($(\".information-detail__body h2\").length==0){        var element=$(\".informacion-adicional__title h3\").html();        $(\".informacion-adicional__title h3\").remove();        $(\".informacion-adicional__title\").prepend(\"<h2>\"+element+\"</h2>\");    }                Foros de Empleo de la UPV/EHU3 de mayo, Bizkaia (inscr\u00edbete para las ofertas de trabajo antes del 18 de abril).  5 de mayo, \u00c1lava.                            JORNADA: Formaci\u00f3n Profesional y Universidad6 de mayo - \u00a1Inscr\u00edbete!                            108 m\u00e1steres universitariosPreinscripci\u00f3n abierta: hasta el 14 de mayo                            KORRIKA 2022Corre a favor del euskera en los kil\u00f3metros de la UPV/EHU.                            Incidencia de la COVID-19 en la comunidad universitariaInformaci\u00f3n facilitada por el Comit\u00e9 de Vigilancia el 06/04/2022            Noticias                                                                                                                         Educaci\u00f3n nutricional, imprescindible para las personas celiacas                                                                                                                                                                                             Una t\u00e9cnica utilizada en an\u00e1lisis de sangre permitir\u00eda diagnosticar tumores en l\u00edquidos pleurales y peritoneales                                                                                                                                                                                             El Congreso Internacional de Derechos Humanos de la UPV/EHU se despide con un alto nivel de participaci\u00f3n y ponencias de primer orden                                                                                                                                                                                             Echa a andar el primer proyecto para producir en el Pa\u00eds Vasco microalgas con fines comerciales                                                                                                                                                                                             Detectan biomarcadores en l\u00e1grima para el diagn\u00f3stico precoz de la enfermedad de Parkinson                                                                                                                                                                                             Los retos de la libertad de expresi\u00f3n en el contexto de los cr\u00edmenes de odio e incitaci\u00f3n al terrorismo: \u201cNormalizaci\u00f3n de discurso de odio\u201d o represi\u00f3n de todo discurso \u201cdesagradable\u201d                                                                     RSS (Abre una nueva ventana) Ver todas las noticias     if($(\".information-detail__body h2\").length==0){        var element=$(\".informacion-adicional__title h3\").html();        $(\".informacion-adicional__title h3\").remove();        $(\".informacion-adicional__title\").prepend(\"<h2>\"+element+\"</h2>\");    }Cathedra                                                                                                                         Ituna 2021: \u00bfCu\u00e1nto sabe y qu\u00e9 opina el alumnado de la UPV/EHU sobre el Concierto Econ\u00f3mico?                                                                                                                                                                                             Aceite de oliva: oro l\u00edquido para combatir la covid-19                                                                                                                                                                                             Retos en el c\u00e1ncer de colon                                                                                                                                                                                             Los cordones democr\u00e1ticos y las estrategias frente a la ultraderecha                                                                                                                                                                                             \u00bfEn qu\u00e9 se parece este liquen ant\u00e1rtico al explorador Ernest Shackelton?                                                                     RSS (Abre una nueva ventana) Ver la secci\u00f3n Cathedra     if($(\".information-detail__body h2\").length==0){        var element=$(\".informacion-adicional__title h3\").html();        $(\".informacion-adicional__title h3\").remove();        $(\".informacion-adicional__title\").prepend(\"<h2>\"+element+\"</h2>\");    }Imagen del d\u00eda                                                                                                                                     \u00a1Qu\u00e9 felicidad!                                                                                                                 Agenda                                                                                                             Exposici\u00f3n: 30 a\u00f1os con cajas-nido06/04/2022- 28/04/2022Donostia / San Sebasti\u00e1n                                                                                                                                                                            Conciertos de EHUabesbatza y EHUorkestra29/04/2022- 30/04/2022                                                                                                                                                                             Empleo Gune 202205/05/2022, 09:30Vitoria-Gasteiz                                                                 RSS (Abre una nueva ventana) Ver todos los eventos     if($(\".information-detail__body h2\").length==0){        var element=$(\".informacion-adicional__title h3\").html();        $(\".informacion-adicional__title h3\").remove();        $(\".informacion-adicional__title\").prepend(\"<h2>\"+element+\"</h2>\");    }                         Transparencia y buen gobierno                         Imprimir banner-portal_transparencia             Sede electr\u00f3nica                        Imprimir banner-egoitza-elektronikoa                 Cursos online                         Imprimir banner-cursos_verano             Enlight                        Imprimir Enlight 2021                 Misiones Euskampus 2.0                         Imprimir Misiones Euskampus 2.0             Cofund ADAGIO                        Imprimir Cofund ADAGIO             EHUagenda 2030                        Imprimir EHUagenda 2030                 Contrataci\u00f3n administrativa                         Imprimir Kontratazio eta erosketak             Plan Estrat\u00e9gico 2018-2021                        Imprimir banner Plan Estrat\u00e9gico 2018-2021             Pr\u00e1cticas y empleo                        Imprimir banner-enplegua             \u00bfYa eres EHUalumni?                        Imprimir banner-ehualumni                 Noticias de la UPV/EHU                         Imprimir banner-campusa             Consejo de Estudiantes                        Imprimir banner-ikasle-kontseilua             Escuela de Doctorado                        Imprimir banner-MDe             Tesis doctorales                        Imprimir banner-tesiak             EHUdenda                        Imprimir banner-ehudenda             Servicio de blogs                        Imprimir banner-ehusfera             EHUtb portal multimedia                        Imprimir banner-ehutb  </div>\n\n"
        }, 
        "WCAG21:contrast-minimum": {
          "Resultado": "Failed", 
          "Texto": "The next ERROR was found: \n\nAccording to the success criteria 1.4.3, the ratio 3 to 1 corresponds to the minimum for text \"in large size\" (18pt or 14 pt bold, or larger). I remind that for the size of normal font the minimum ratio is 4,5 to 1.On the code: \n\n<span class=\"hide-accessible\">Mostrar/ocultar subp\u00e1ginas</span>\n\n<span class=\"hide-accessible\">Mostrar/ocultar subp\u00e1ginas</span>\n\n<span class=\"hide-accessible\">Mostrar/ocultar subp\u00e1ginas</span>\n\n<span class=\"hide-accessible\">Mostrar/ocultar subp\u00e1ginas</span>\n\n<span class=\"hide-accessible\">Mostrar/ocultar subp\u00e1ginas</span>\n\n"
        }, 
        "WCAG21:info-and-relationships": {
          "Resultado": "Passed", 
          "Texto": "The next CORRECTION CHECK was found: \n\nThe <label> elements associated to the <input> elements\u00a0allow the Assistive Technologies users to identify the label that contextualize an edition field. The explicit association is done by the pair of id and dor attributes, respectively, from the <input> and <label> elements."
        }, 
        "WCAG21:labels-or-instructions": {
          "Resultado": "Passed", 
          "Texto": "The next CORRECTION CHECK was found: \n\nThe <label> elements associated to the <input> elements\u00a0allow the Assistive Technologies users to identify the label that contextualize an edition field. The explicit association is done by the pair of id and dor attributes, respectively, from the <input> and <label> elements."
        }, 
        "WCAG21:link-purpose-in-context": {
          "Resultado": "Failed", 
          "Texto": "The next ERROR was found: \n\nThe title attribute is used to provide additional information to that one existent in the text link. The attribute title and the text of the link should be sufficient to understand the link purpose.On the code: \n\n<a class=\"breadcrumb-link\" href=\"https://www.ehu.eus/es\" title=\"UPV/EHU\">            UPV/EHU            </a>\n\n<a class=\"twitter\" href=\"https://twitter.com/upvehu\" target=\"blank\" title=\"Twitter\">Twitter</a>\n\n<a class=\"facebook\" href=\"https://www.facebook.com/upv.ehu\" target=\"blank\" title=\"Facebook\">Facebook</a>\n\n<a class=\"instagram\" href=\"https://www.instagram.com/upvehu_gara/\" target=\"blank\" title=\"Instagram\">Instagram</a>\n\n<a class=\"linkedin\" href=\"https://www.linkedin.com/edu/school?id=12231&amp;trk=edu-cp-title\" target=\"blank\" title=\"Linkedin\">Linkedin</a>\n\n<a class=\"youtube\" href=\"https://www.youtube.com/user/upvehu\" target=\"blank\" title=\"Youtube\">Youtube</a>\n\n<a class=\"vimeo\" href=\"https://vimeo.com/UPVEHU/ALBUMS\" target=\"blank\" title=\"Vimeo\">Vimeo</a>\n\n<a href=\"https://euskampus.eus/es/actualidad/noticias/euskampus-fundazioa-lanza-el-programa-2022-201cmisiones-euskampus-2-0201d\" title=\"Misiones Euskampus 2.0\">    Misiones Euskampus 2.0                         </a>\n\n"
        }, 
        "WCAG21:name-role-value": {
          "Resultado": "Passed", 
          "Texto": "The next CORRECTION CHECK was found: \n\nThe <label> elements associated to the <input> elements\u00a0allow the Assistive Technologies users to identify the label that contextualize an edition field. The explicit association is done by the pair of id and dor attributes, respectively, from the <input> and <label> elements."
        }, 
        "WCAG21:non-text-content": {
          "Resultado": "Failed", 
          "Texto": "The next ERROR was found: \n\nVerify if the alternative textual equivalent found in the graphic buttons serves the equal information or function performed by the graphic button on the page.On the code: \n\n<img class=\"span4\" alt=\" \" src=\"https://www.ehu.eus/documents/10136/0/katagorria_dest.jpg/5af35a0e-77a0-e820-5913-fd0421b72c0b?t=1649844150220\"/documents/10136/0/katagorria_dest.jpg/5af35a0e-77a0-e820-5913-fd0421b72c0b?t=1649844150220\">\n\n---------------------------------------- \n\n The next WARNING was found: \n\nThe use of null or empty alternative texts in HTML is a common practice for images classified as decorative. However, all images classified as decorative must be affixed via CSS and not via HTML.On the code: \n\n<img class=\"span4\" src=\"https://www.ehu.eus/documents/10136/34166400/master_egunak_dest_new.jpg/3c37236c-70c1-57d5-e73e-c2bde6e973c0?t=1647867348115\"/documents/10136/34166400/master_egunak_dest_new.jpg/3c37236c-70c1-57d5-e73e-c2bde6e973c0?t=1647867348115\" alt=\"\">\n\n<img alt=\"\" src=\"https://www.ehu.eus/o/ehu-theme/images/common/rss.png\" style=\"background-image: url('https://www.ehu.eus/o/ehu-theme/images/common/rss.png'); background-position: 50% -1326px; background-repeat: no-repeat; height: 16px; width: 16px;\">\n\n<img alt=\"\" src=\"https://www.ehu.eus/o/ehu-theme/images/common/rss.png\" style=\"background-image: url('https://www.ehu.eus/o/ehu-theme/images/common/rss.png'); background-position: 50% -1326px; background-repeat: no-repeat; height: 16px; width: 16px;\">\n\n<img alt=\"\" src=\"https://www.ehu.eus/o/ehu-theme/images/common/rss.png\" style=\"background-image: url('https://www.ehu.eus/o/ehu-theme/images/common/rss.png'); background-position: 50% -1326px; background-repeat: no-repeat; height: 16px; width: 16px;\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/banner-transparencia.jpg/0d1d3ccb-8762-4feb-adb0-d10727171982?t=1505904032000\"/documents/10136/1002378/banner-transparencia.jpg/0d1d3ccb-8762-4feb-adb0-d10727171982?t=1505904032000\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/sede-electronica-2021_banner.jpg/7f623d5b-9e70-5472-0fac-5fa284008576?t=1623148446803\"/documents/10136/1002378/sede-electronica-2021_banner.jpg/7f623d5b-9e70-5472-0fac-5fa284008576?t=1623148446803\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/cusos-verano-2021_banner.jpg/db255ee4-c787-6a75-7c61-76762bbf9fa1?t=1618826107271\"/documents/10136/1002378/cusos-verano-2021_banner.jpg/db255ee4-c787-6a75-7c61-76762bbf9fa1?t=1618826107271\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/banner_enlight-2021.gif/d7af04e7-5534-82bf-875b-17c607b19c2d?t=1626155371179\"/documents/10136/1002378/banner_enlight-2021.gif/d7af04e7-5534-82bf-875b-17c607b19c2d?t=1626155371179\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/banner_euskampus-play.gif/0e21204d-42b8-f9e6-85b5-a1dba57cf9a1?t=1642164110891\"/documents/10136/1002378/banner_euskampus-play.gif/0e21204d-42b8-f9e6-85b5-a1dba57cf9a1?t=1642164110891\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/banner-ADAGIO2.jpg/fb3fe9d3-377e-31ab-08aa-1b48b678a932?t=1646987281956\"/documents/10136/1002378/banner-ADAGIO2.jpg/fb3fe9d3-377e-31ab-08aa-1b48b678a932?t=1646987281956\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/banner_ehuagenda+2030_2.jpg/09a2d35b-648a-0b3b-2cae-dd5820862cca?t=1561117076000\"/documents/10136/1002378/banner_ehuagenda+2030_2.jpg/09a2d35b-648a-0b3b-2cae-dd5820862cca?t=1561117076000\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/Contrataci%C3%B3n+y+compras.jpg/b46271e8-6cc4-50c1-5428-73b97f65a2bb?t=1522240229000\"/documents/10136/1002378/Contrataci%C3%B3n+y+compras.jpg/b46271e8-6cc4-50c1-5428-73b97f65a2bb?t=1522240229000\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/banner_plan_estrategico_2019.jpg/7cd0b568-c46d-857d-60ab-26dd27d8f4d3?t=1570007113000\"/documents/10136/1002378/banner_plan_estrategico_2019.jpg/7cd0b568-c46d-857d-60ab-26dd27d8f4d3?t=1570007113000\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/banner-empleo-practicas.png/c12bf422-f4d9-4242-a144-7834d5afc2e5?t=1412689849000\"/documents/10136/1002378/banner-empleo-practicas.png/c12bf422-f4d9-4242-a144-7834d5afc2e5?t=1412689849000\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/ehualumni.jpg/b4c83411-f367-49d8-a3cb-30d7e215e7df?t=1494941545000\"/documents/10136/1002378/ehualumni.jpg/b4c83411-f367-49d8-a3cb-30d7e215e7df?t=1494941545000\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/banner-campusa.jpg/102e03d3-3212-4d7f-8193-9cbc1184757d?t=1421251115000\"/documents/10136/1002378/banner-campusa.jpg/102e03d3-3212-4d7f-8193-9cbc1184757d?t=1421251115000\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/banner-consejo-estudiantes-es.png/e80ca8dd-3619-4a62-92a0-f17c46073b6c?t=1412689815000\"/documents/10136/1002378/banner-consejo-estudiantes-es.png/e80ca8dd-3619-4a62-92a0-f17c46073b6c?t=1412689815000\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/banner_escuela_doctorado.jpg/d93bee73-2431-c4c9-3a82-6c920e411aea?t=1594983278754\"/documents/10136/1002378/banner_escuela_doctorado.jpg/d93bee73-2431-c4c9-3a82-6c920e411aea?t=1594983278754\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/banner-birretes.png/29164d50-c728-4ebd-8f48-ec0d575bedf3?t=1412689808000\"/documents/10136/1002378/banner-birretes.png/29164d50-c728-4ebd-8f48-ec0d575bedf3?t=1412689808000\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/522485/1339603/ehudenda.jpg/e5483a92-f918-46eb-878a-c4cfc56a1a16?t=1422368804000\"/documents/522485/1339603/ehudenda.jpg/e5483a92-f918-46eb-878a-c4cfc56a1a16?t=1422368804000\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/10136/1002378/EHUsfera_2.jpg/bfcbc44f-0e9a-4aa4-af8f-044ded707eda?t=1443006941000\"/documents/10136/1002378/EHUsfera_2.jpg/bfcbc44f-0e9a-4aa4-af8f-044ded707eda?t=1443006941000\" alt=\"\">\n\n<img src=\"https://www.ehu.eus/documents/522485/1339603/ehutb.jpg/5207a004-2837-41a3-ac72-9159f8291735?t=1422368773000\"/documents/522485/1339603/ehutb.jpg/5207a004-2837-41a3-ac72-9159f8291735?t=1422368773000\" alt=\"\">\n\n---------------------------------------- \n\n The next CORRECTION CHECK was found: \n\nThe <label> elements associated to the <input> elements\u00a0allow the Assistive Technologies users to identify the label that contextualize an edition field. The explicit association is done by the pair of id and dor attributes, respectively, from the <input> and <label> elements."
        }, 
        "WCAG21:on-input": {
          "Resultado": "Passed", 
          "Texto": "The next CORRECTION CHECK was found: \n\nAfter\u00a0being filled, it is necessary to submit the form data to the server. This is the function of the submit button."
        }
      }, 
      "RESULTADO": "6.3", 
      "Tester_Name": "Access_Monitor"
    }
    
    return informe

@app.route('/informe2/')
def informe2():
    informe = {
      "Cases": {
        "WCAG21:bypass-blocks": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"input element label, type of \"text\", is not positioned close to control.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 1972, Column 5</em>: \"<code class=\"input\">&lt;input  class=\"field search-input search-portlet-keywords-input form-control\"  id=\"_com_liferay_port ...</code>\".\n\n"
        }, 
        "WCAG21:consistent-identification": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"script may use color alone.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 112, Column 2</em>: \"<code class=\"input\">&lt;script async src=\"https://www.googletagmanager.com/gtag/js?id=G-PF5W7J2G9S\"&gt;&lt;/script&gt;</code>\".\n\nLINE <em>Line 113, Column 2</em>: \"<code class=\"input\">&lt;script&gt;\n\t\twindow.dataLayer = window.dataLayer || [];\n\t\tfunction gtag(){dataLayer.push(arguments); ...</code>\".\n\nLINE <em>Line 120, Column 2</em>: \"<code class=\"input\">&lt;script&gt;(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n\tnew Date().getTime(),event:'gtm ...</code>\".\n\nLINE <em>Line 191, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" src=\"/combo?browserId=other&amp;minifierType=js&amp;languageId=es_ES&amp;b= ...</code>\".\n\nLINE <em>Line 280, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"temporary\" type=\"text/javascript\"&gt;\n\t// &lt;![CDATA[\n\t\tvar Liferay = Liferay | ...</code>\".\n\nLINE <em>Line 603, Column 1</em>: \"<code class=\"input\">&lt;script src=\"/o/js_loader_config?t=1648628130409\" type=\"text/javascript\"&gt;&lt;/script&gt;</code>\".\n\nLINE <em>Line 604, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" src=\"/combo?browserId=other&amp;minifierType=js&amp;languageId=es_ES&amp;b= ...</code>\".\n\nLINE <em>Line 605, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" src=\"/combo?browserId=other&amp;minifierType=js&amp;languageId=es_ES&amp;b= ...</code>\".\n\nLINE <em>Line 606, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" src=\"/combo?browserId=other&amp;minifierType=js&amp;languageId=es_ES&amp;b= ...</code>\".\n\nLINE <em>Line 613, Column 2</em>: \"<code class=\"input\">&lt;script data-senna-track=\"temporary\" src=\"/o/js_bundle_config?t=1648716674805\" type=\"text/javascript ...</code>\".\n\nLINE <em>Line 616, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"temporary\" type=\"text/javascript\"&gt;\n\t// &lt;![CDATA[\n\t\t\n\t\t\t\n\t\t\t\t\n\t\t\n\n\t\t\n\n\t\t\n\t/ ...</code>\".\n\nLINE <em>Line 639, Column 5</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" id=\"googleAnalyticsScript\" type=\"text/javascript\"&gt;\n\t\t\t\t\t(functi ...</code>\".\n\nLINE <em>Line 952, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\nLiferay.on(\n\t'ddmFieldBlur', function(event) {\n\t\tif (wi ...</code>\".\n\nLINE <em>Line 1052, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"temporary\" type=\"text/javascript\"&gt;\n\tif (window.Analytics) {\n\t\twindow._com_ ...</code>\".\n\nLINE <em>Line 2142, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n\t(function() {\n\t\tvar select = document.getElementById('_com_liferay_portal_search_web_portl ...</code>\".\n\nLINE <em>Line 2211, Column 2</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\n\n\t\twindow._com_liferay_portal_search_web_portlet_Searc ...</code>\".\n\nLINE <em>Line 2296, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\nAUI().use('liferay-form', function(A) {(function() {var ...</code>\".\n\nLINE <em>Line 3664, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n    if($(\".information-detail__body h2\").length==0){\n        var element=$(\".informacion-ad ...</code>\".\n\nLINE <em>Line 6524, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n    if($(\".information-detail__body h2\").length==0){\n        var element=$(\".informacion-ad ...</code>\".\n\nLINE <em>Line 7522, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n    if($(\".information-detail__body h2\").length==0){\n        var element=$(\".informacion-ad ...</code>\".\n\nLINE <em>Line 8946, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n    if($(\".information-detail__body h2\").length==0){\n        var element=$(\".informacion-ad ...</code>\".\n\nLINE <em>Line 14063, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\n\n\t\n\t\t\n\n\t\t\t\n\n\t\t\t\n\t\t\n\t\n\n\tLiferay.BrowserSelectors.run();\n ...</code>\".\n\nLINE <em>Line 14092, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n\t// &lt;![CDATA[\n\n\t\t\n\n\t\tLiferay.currentURL = '\\x2fes\\x2fhome';\n\t\tLifera ...</code>\".\n\nLINE <em>Line 14109, Column 2</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n\t\t// &lt;![CDATA[\n\t\t\t\n\t\t\t\t\n\n\t\t\t\t\n\t\t\t\n\t\t// ]]&gt;\n\t\n\n\n\n\n\n\n\n&lt;/script&gt;</code>\".\n\nLINE <em>Line 14140, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\n\n\t\t\t\t\t\t\t\tfunction _com_liferay_asset_publisher_web_por ...</code>\".\n\nLINE <em>Line 14813, Column 1</em>: \"<code class=\"input\">&lt;script src=\"https://www.ehu.eus/o/ehu-theme/js/main.js?browserId=other&amp;amp;minifierType=js&amp;amp;lang ...</code>\".\n\nLINE <em>Line 14818, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n\t// &lt;![CDATA[\n\t\tAUI().use(\n\t\t\t'aui-base',\n\t\t\tfunction(A) {\n\t\t\t\tvar f ...</code>\".\n\nLINE <em>Line 14831, Column 10</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\nLiferay.Loader.require('frontend-js-tooltip-support-web ...</code>\".\n\n"
        }, 
        "WCAG21:consistent-navigation": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"input possibly using color alone.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 1972, Column 5</em>: \"<code class=\"input\">&lt;input  class=\"field search-input search-portlet-keywords-input form-control\"  id=\"_com_liferay_port ...</code>\".\n\nLINE <em>Line 13880, Column 103</em>: \"<code class=\"input\">&lt;input hidden type=\"submit\"/&gt;</code>\".\n\n"
        }, 
        "WCAG21:error-identification": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"Image may contain text that is not in Alt text.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 1456, Column 6</em>: \"<code class=\"input\">&lt;img class=\"logo\" src=\"https://www.ehu.eus/o/ehu-theme/images/custom/logo.png\" alt=\"Universidad del  ...</code>\".\n\nLINE <em>Line 1461, Column 6</em>: \"<code class=\"input\">&lt;img class=\"logo-guest\" src=\"https://www.ehu.eus/o/ehu-theme/images/custom/logo-ucrania.png\" alt=\"UP ...</code>\".\n\nLINE <em>Line 4036, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/foroempleo_destacados_.jpg/d399eeb7-ec93-e7b7-3d30 ...</code>\".\n\nLINE <em>Line 4397, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/formacion_profesional_dest.jpg/1def6bda-616d-0b09- ...</code>\".\n\nLINE <em>Line 4758, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/master_egunak_dest_new.jpg/3c37236c-70c1-57d5-e73e ...</code>\".\n\nLINE <em>Line 5119, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/KORRIKA+2022.jpg/79b4122f-389f-304d-4234-abf7a5271 ...</code>\".\n\nLINE <em>Line 5480, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/13743974/Coronavirus.jpg/ec342006-3a76-075d-1b53-00df150654 ...</code>\".\n\nLINE <em>Line 7956, Column 13</em>: \"<code class=\"input\">&lt;img class=\"span4\" alt=' ' src='/documents/10136/0/katagorria_dest.jpg/5af35a0e-77a0-e820-5913-fd042 ...</code>\".\n\nLINE <em>Line 9464, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner-transparencia.jpg/0d1d3ccb-8762-4feb-adb0-d10727171982?t=1 ...</code>\".\n\nLINE <em>Line 9714, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/sede-electronica-2021_banner.jpg/7f623d5b-9e70-5472-0fac-5fa28400 ...</code>\".\n\nLINE <em>Line 9962, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/cusos-verano-2021_banner.jpg/db255ee4-c787-6a75-7c61-76762bbf9fa1 ...</code>\".\n\nLINE <em>Line 10212, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner_enlight-2021.gif/d7af04e7-5534-82bf-875b-17c607b19c2d?t=16 ...</code>\".\n\nLINE <em>Line 10460, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner_euskampus-play.gif/0e21204d-42b8-f9e6-85b5-a1dba57cf9a1?t= ...</code>\".\n\nLINE <em>Line 10710, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner-ADAGIO2.jpg/fb3fe9d3-377e-31ab-08aa-1b48b678a932?t=1646987 ...</code>\".\n\nLINE <em>Line 10958, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner_ehuagenda+2030_2.jpg/09a2d35b-648a-0b3b-2cae-dd5820862cca? ...</code>\".\n\nLINE <em>Line 11206, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/Contrataci%C3%B3n+y+compras.jpg/b46271e8-6cc4-50c1-5428-73b97f65a ...</code>\".\n\nLINE <em>Line 11456, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner_plan_estrategico_2019.jpg/7cd0b568-c46d-857d-60ab-26dd27d8 ...</code>\".\n\nLINE <em>Line 11704, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner-empleo-practicas.png/c12bf422-f4d9-4242-a144-7834d5afc2e5? ...</code>\".\n\nLINE <em>Line 11952, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/ehualumni.jpg/b4c83411-f367-49d8-a3cb-30d7e215e7df?t=149494154500 ...</code>\".\n\nLINE <em>Line 12200, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner-campusa.jpg/102e03d3-3212-4d7f-8193-9cbc1184757d?t=1421251 ...</code>\".\n\nLINE <em>Line 12450, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner-consejo-estudiantes-es.png/e80ca8dd-3619-4a62-92a0-f17c460 ...</code>\".\n\nLINE <em>Line 12698, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner_escuela_doctorado.jpg/d93bee73-2431-c4c9-3a82-6c920e411aea ...</code>\".\n\nLINE <em>Line 12946, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner-birretes.png/29164d50-c728-4ebd-8f48-ec0d575bedf3?t=141268 ...</code>\".\n\nLINE <em>Line 13194, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/522485/1339603/ehudenda.jpg/e5483a92-f918-46eb-878a-c4cfc56a1a16?t=142236880400 ...</code>\".\n\nLINE <em>Line 13442, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/EHUsfera_2.jpg/bfcbc44f-0e9a-4aa4-af8f-044ded707eda?t=14430069410 ...</code>\".\n\nLINE <em>Line 13690, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/522485/1339603/ehutb.jpg/5207a004-2837-41a3-ac72-9159f8291735?t=1422368773000\"  ...</code>\".\n\n"
        }, 
        "WCAG21:error-suggestion": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"script may cause screen flicker.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 112, Column 2</em>: \"<code class=\"input\">&lt;script async src=\"https://www.googletagmanager.com/gtag/js?id=G-PF5W7J2G9S\"&gt;&lt;/script&gt;</code>\".\n\nLINE <em>Line 113, Column 2</em>: \"<code class=\"input\">&lt;script&gt;\n\t\twindow.dataLayer = window.dataLayer || [];\n\t\tfunction gtag(){dataLayer.push(arguments); ...</code>\".\n\nLINE <em>Line 120, Column 2</em>: \"<code class=\"input\">&lt;script&gt;(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n\tnew Date().getTime(),event:'gtm ...</code>\".\n\nLINE <em>Line 191, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" src=\"/combo?browserId=other&amp;minifierType=js&amp;languageId=es_ES&amp;b= ...</code>\".\n\nLINE <em>Line 280, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"temporary\" type=\"text/javascript\"&gt;\n\t// &lt;![CDATA[\n\t\tvar Liferay = Liferay | ...</code>\".\n\nLINE <em>Line 603, Column 1</em>: \"<code class=\"input\">&lt;script src=\"/o/js_loader_config?t=1648628130409\" type=\"text/javascript\"&gt;&lt;/script&gt;</code>\".\n\nLINE <em>Line 604, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" src=\"/combo?browserId=other&amp;minifierType=js&amp;languageId=es_ES&amp;b= ...</code>\".\n\nLINE <em>Line 605, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" src=\"/combo?browserId=other&amp;minifierType=js&amp;languageId=es_ES&amp;b= ...</code>\".\n\nLINE <em>Line 606, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" src=\"/combo?browserId=other&amp;minifierType=js&amp;languageId=es_ES&amp;b= ...</code>\".\n\nLINE <em>Line 613, Column 2</em>: \"<code class=\"input\">&lt;script data-senna-track=\"temporary\" src=\"/o/js_bundle_config?t=1648716674805\" type=\"text/javascript ...</code>\".\n\nLINE <em>Line 616, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"temporary\" type=\"text/javascript\"&gt;\n\t// &lt;![CDATA[\n\t\t\n\t\t\t\n\t\t\t\t\n\t\t\n\n\t\t\n\n\t\t\n\t/ ...</code>\".\n\nLINE <em>Line 639, Column 5</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" id=\"googleAnalyticsScript\" type=\"text/javascript\"&gt;\n\t\t\t\t\t(functi ...</code>\".\n\nLINE <em>Line 952, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\nLiferay.on(\n\t'ddmFieldBlur', function(event) {\n\t\tif (wi ...</code>\".\n\nLINE <em>Line 1052, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"temporary\" type=\"text/javascript\"&gt;\n\tif (window.Analytics) {\n\t\twindow._com_ ...</code>\".\n\nLINE <em>Line 2142, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n\t(function() {\n\t\tvar select = document.getElementById('_com_liferay_portal_search_web_portl ...</code>\".\n\nLINE <em>Line 2211, Column 2</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\n\n\t\twindow._com_liferay_portal_search_web_portlet_Searc ...</code>\".\n\nLINE <em>Line 2296, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\nAUI().use('liferay-form', function(A) {(function() {var ...</code>\".\n\nLINE <em>Line 3664, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n    if($(\".information-detail__body h2\").length==0){\n        var element=$(\".informacion-ad ...</code>\".\n\nLINE <em>Line 6524, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n    if($(\".information-detail__body h2\").length==0){\n        var element=$(\".informacion-ad ...</code>\".\n\nLINE <em>Line 7522, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n    if($(\".information-detail__body h2\").length==0){\n        var element=$(\".informacion-ad ...</code>\".\n\nLINE <em>Line 8946, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n    if($(\".information-detail__body h2\").length==0){\n        var element=$(\".informacion-ad ...</code>\".\n\nLINE <em>Line 14063, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\n\n\t\n\t\t\n\n\t\t\t\n\n\t\t\t\n\t\t\n\t\n\n\tLiferay.BrowserSelectors.run();\n ...</code>\".\n\nLINE <em>Line 14092, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n\t// &lt;![CDATA[\n\n\t\t\n\n\t\tLiferay.currentURL = '\\x2fes\\x2fhome';\n\t\tLifera ...</code>\".\n\nLINE <em>Line 14109, Column 2</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n\t\t// &lt;![CDATA[\n\t\t\t\n\t\t\t\t\n\n\t\t\t\t\n\t\t\t\n\t\t// ]]&gt;\n\t\n\n\n\n\n\n\n\n&lt;/script&gt;</code>\".\n\nLINE <em>Line 14140, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\n\n\t\t\t\t\t\t\t\tfunction _com_liferay_asset_publisher_web_por ...</code>\".\n\nLINE <em>Line 14813, Column 1</em>: \"<code class=\"input\">&lt;script src=\"https://www.ehu.eus/o/ehu-theme/js/main.js?browserId=other&amp;amp;minifierType=js&amp;amp;lang ...</code>\".\n\nLINE <em>Line 14818, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n\t// &lt;![CDATA[\n\t\tAUI().use(\n\t\t\t'aui-base',\n\t\t\tfunction(A) {\n\t\t\t\tvar f ...</code>\".\n\nLINE <em>Line 14831, Column 10</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\nLiferay.Loader.require('frontend-js-tooltip-support-web ...</code>\".\n\n"
        }, 
        "WCAG21:headings-and-labels": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"Image may contain text with poor contrast.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 1456, Column 6</em>: \"<code class=\"input\">&lt;img class=\"logo\" src=\"https://www.ehu.eus/o/ehu-theme/images/custom/logo.png\" alt=\"Universidad del  ...</code>\".\n\nLINE <em>Line 1461, Column 6</em>: \"<code class=\"input\">&lt;img class=\"logo-guest\" src=\"https://www.ehu.eus/o/ehu-theme/images/custom/logo-ucrania.png\" alt=\"UP ...</code>\".\n\nLINE <em>Line 4036, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/foroempleo_destacados_.jpg/d399eeb7-ec93-e7b7-3d30 ...</code>\".\n\nLINE <em>Line 4397, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/formacion_profesional_dest.jpg/1def6bda-616d-0b09- ...</code>\".\n\nLINE <em>Line 4758, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/master_egunak_dest_new.jpg/3c37236c-70c1-57d5-e73e ...</code>\".\n\nLINE <em>Line 5119, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/KORRIKA+2022.jpg/79b4122f-389f-304d-4234-abf7a5271 ...</code>\".\n\nLINE <em>Line 5480, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/13743974/Coronavirus.jpg/ec342006-3a76-075d-1b53-00df150654 ...</code>\".\n\nLINE <em>Line 6483, Column 184</em>: \"<code class=\"input\">&lt;img alt=\"\" src=\"https://www.ehu.eus/o/ehu-theme/images/common/rss.png\" style=\"background-image: url ...</code>\".\n\nLINE <em>Line 7481, Column 184</em>: \"<code class=\"input\">&lt;img alt=\"\" src=\"https://www.ehu.eus/o/ehu-theme/images/common/rss.png\" style=\"background-image: url ...</code>\".\n\nLINE <em>Line 7956, Column 13</em>: \"<code class=\"input\">&lt;img class=\"span4\" alt=' ' src='/documents/10136/0/katagorria_dest.jpg/5af35a0e-77a0-e820-5913-fd042 ...</code>\".\n\nLINE <em>Line 8905, Column 148</em>: \"<code class=\"input\">&lt;img alt=\"\" src=\"https://www.ehu.eus/o/ehu-theme/images/common/rss.png\" style=\"background-image: url ...</code>\".\n\nLINE <em>Line 9464, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner-transparencia.jpg/0d1d3ccb-8762-4feb-adb0-d10727171982?t=1 ...</code>\".\n\nLINE <em>Line 9714, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/sede-electronica-2021_banner.jpg/7f623d5b-9e70-5472-0fac-5fa28400 ...</code>\".\n\nLINE <em>Line 9962, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/cusos-verano-2021_banner.jpg/db255ee4-c787-6a75-7c61-76762bbf9fa1 ...</code>\".\n\nLINE <em>Line 10212, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner_enlight-2021.gif/d7af04e7-5534-82bf-875b-17c607b19c2d?t=16 ...</code>\".\n\nLINE <em>Line 10460, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner_euskampus-play.gif/0e21204d-42b8-f9e6-85b5-a1dba57cf9a1?t= ...</code>\".\n\nLINE <em>Line 10710, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner-ADAGIO2.jpg/fb3fe9d3-377e-31ab-08aa-1b48b678a932?t=1646987 ...</code>\".\n\nLINE <em>Line 10958, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner_ehuagenda+2030_2.jpg/09a2d35b-648a-0b3b-2cae-dd5820862cca? ...</code>\".\n\nLINE <em>Line 11206, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/Contrataci%C3%B3n+y+compras.jpg/b46271e8-6cc4-50c1-5428-73b97f65a ...</code>\".\n\nLINE <em>Line 11456, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner_plan_estrategico_2019.jpg/7cd0b568-c46d-857d-60ab-26dd27d8 ...</code>\".\n\nLINE <em>Line 11704, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner-empleo-practicas.png/c12bf422-f4d9-4242-a144-7834d5afc2e5? ...</code>\".\n\nLINE <em>Line 11952, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/ehualumni.jpg/b4c83411-f367-49d8-a3cb-30d7e215e7df?t=149494154500 ...</code>\".\n\nLINE <em>Line 12200, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner-campusa.jpg/102e03d3-3212-4d7f-8193-9cbc1184757d?t=1421251 ...</code>\".\n\nLINE <em>Line 12450, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner-consejo-estudiantes-es.png/e80ca8dd-3619-4a62-92a0-f17c460 ...</code>\".\n\nLINE <em>Line 12698, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner_escuela_doctorado.jpg/d93bee73-2431-c4c9-3a82-6c920e411aea ...</code>\".\n\nLINE <em>Line 12946, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/banner-birretes.png/29164d50-c728-4ebd-8f48-ec0d575bedf3?t=141268 ...</code>\".\n\nLINE <em>Line 13194, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/522485/1339603/ehudenda.jpg/e5483a92-f918-46eb-878a-c4cfc56a1a16?t=142236880400 ...</code>\".\n\nLINE <em>Line 13442, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/10136/1002378/EHUsfera_2.jpg/bfcbc44f-0e9a-4aa4-af8f-044ded707eda?t=14430069410 ...</code>\".\n\nLINE <em>Line 13690, Column 4</em>: \"<code class=\"input\">&lt;img src=\"/documents/522485/1339603/ehutb.jpg/5207a004-2837-41a3-ac72-9159f8291735?t=1422368773000\"  ...</code>\".\n\n"
        }, 
        "WCAG21:images-of-text": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"Unicode right-to-left marks or left-to-right marks may be required.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 1077, Column 1</em>: \"<code class=\"input\">&lt;body class=\" controls-visible  yui3-skin-sam guest-site signed-out public-page site es_ES\"&gt;\n\n\t&lt;no ...</code>\".\n\n"
        }, 
        "WCAG21:info-and-relationships": {
          "Resultado": "Cannot Tell", 
          "Texto": "The next WARNING was found: \"p element may be misused (could be a header).\". The warning was in the following line(s): \n\n \"LINE <em>Line 4038, Column 8</em>: \"<code class=\"input\">&lt;p class=\"card-title\"&gt;&lt;strong&gt;\n\t\t\t\t\t\t\t\tForos de Empleo de la UPV/EHU\n\t\t\t\t\t\t\t&lt;/strong&gt;&lt;/p&gt;</code>\".\n\nLINE <em>Line 4399, Column 8</em>: \"<code class=\"input\">&lt;p class=\"card-title\"&gt;&lt;strong&gt;\n\t\t\t\t\t\t\t\tJORNADA: Formaci\u00f3n Profesional y Universidad\n\t\t\t\t\t\t\t&lt;/strong ...</code>\".\n\nLINE <em>Line 4760, Column 8</em>: \"<code class=\"input\">&lt;p class=\"card-title\"&gt;&lt;strong&gt;\n\t\t\t\t\t\t\t\t108 m\u00e1steres universitarios\n\t\t\t\t\t\t\t&lt;/strong&gt;&lt;/p&gt;</code>\".\n\nLINE <em>Line 5121, Column 8</em>: \"<code class=\"input\">&lt;p class=\"card-title\"&gt;&lt;strong&gt;\n\t\t\t\t\t\t\t\tKORRIKA 2022\n\t\t\t\t\t\t\t&lt;/strong&gt;&lt;/p&gt;</code>\".\n\nLINE <em>Line 5482, Column 8</em>: \"<code class=\"input\">&lt;p class=\"card-title\"&gt;&lt;strong&gt;\n\t\t\t\t\t\t\t\tIncidencia de la COVID-19 en la comunidad universitaria\n\t\t\t\t\t ...</code>\".\n\nLINE <em>Line 7958, Column 17</em>: \"<code class=\"input\">&lt;p class=\"card-title\"&gt;&lt;strong&gt;\u00a1Qu\u00e9 felicidad!&lt;/strong&gt;&lt;/p&gt;</code>\".\n\n---------------------------------------- \n\n A POTENTIAL PROBLEM was found: \"Alt text is not empty and image may be decorative.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 1456, Column 6</em>: \"<code class=\"input\">&lt;img class=\"logo\" src=\"https://www.ehu.eus/o/ehu-theme/images/custom/logo.png\" alt=\"Universidad del  ...</code>\".\n\nLINE <em>Line 1461, Column 6</em>: \"<code class=\"input\">&lt;img class=\"logo-guest\" src=\"https://www.ehu.eus/o/ehu-theme/images/custom/logo-ucrania.png\" alt=\"UP ...</code>\".\n\nLINE <em>Line 4036, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/foroempleo_destacados_.jpg/d399eeb7-ec93-e7b7-3d30 ...</code>\".\n\nLINE <em>Line 4397, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/formacion_profesional_dest.jpg/1def6bda-616d-0b09- ...</code>\".\n\nLINE <em>Line 5119, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/KORRIKA+2022.jpg/79b4122f-389f-304d-4234-abf7a5271 ...</code>\".\n\nLINE <em>Line 5480, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/13743974/Coronavirus.jpg/ec342006-3a76-075d-1b53-00df150654 ...</code>\".\n\n"
        }, 
        "WCAG21:keyboard": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"Visual lists may not be properly marked.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 1077, Column 1</em>: \"<code class=\"input\">&lt;body class=\" controls-visible  yui3-skin-sam guest-site signed-out public-page site es_ES\"&gt;\n\n\t&lt;no ...</code>\".\n\n"
        }, 
        "WCAG21:labels-or-instructions": {
          "Resultado": "Failed", 
          "Texto": "The next ERROR was found: \"Label text is empty.\". You can solve it with: \"\nRepair: Add text to the label element.\n\n           \n           \". The error was in the following line(s): \n\n \"LINE <em>Line 13880, Column 103</em>: \"<code class=\"input\">&lt;input hidden type=\"submit\"/&gt;</code>\"\n\n---------------------------------------- \n\n A POTENTIAL PROBLEM was found: \"script user interface may not be accessible.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 112, Column 2</em>: \"<code class=\"input\">&lt;script async src=\"https://www.googletagmanager.com/gtag/js?id=G-PF5W7J2G9S\"&gt;&lt;/script&gt;</code>\".\n\nLINE <em>Line 113, Column 2</em>: \"<code class=\"input\">&lt;script&gt;\n\t\twindow.dataLayer = window.dataLayer || [];\n\t\tfunction gtag(){dataLayer.push(arguments); ...</code>\".\n\nLINE <em>Line 120, Column 2</em>: \"<code class=\"input\">&lt;script&gt;(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n\tnew Date().getTime(),event:'gtm ...</code>\".\n\nLINE <em>Line 191, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" src=\"/combo?browserId=other&amp;minifierType=js&amp;languageId=es_ES&amp;b= ...</code>\".\n\nLINE <em>Line 280, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"temporary\" type=\"text/javascript\"&gt;\n\t// &lt;![CDATA[\n\t\tvar Liferay = Liferay | ...</code>\".\n\nLINE <em>Line 603, Column 1</em>: \"<code class=\"input\">&lt;script src=\"/o/js_loader_config?t=1648628130409\" type=\"text/javascript\"&gt;&lt;/script&gt;</code>\".\n\nLINE <em>Line 604, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" src=\"/combo?browserId=other&amp;minifierType=js&amp;languageId=es_ES&amp;b= ...</code>\".\n\nLINE <em>Line 605, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" src=\"/combo?browserId=other&amp;minifierType=js&amp;languageId=es_ES&amp;b= ...</code>\".\n\nLINE <em>Line 606, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" src=\"/combo?browserId=other&amp;minifierType=js&amp;languageId=es_ES&amp;b= ...</code>\".\n\nLINE <em>Line 613, Column 2</em>: \"<code class=\"input\">&lt;script data-senna-track=\"temporary\" src=\"/o/js_bundle_config?t=1648716674805\" type=\"text/javascript ...</code>\".\n\nLINE <em>Line 616, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"temporary\" type=\"text/javascript\"&gt;\n\t// &lt;![CDATA[\n\t\t\n\t\t\t\n\t\t\t\t\n\t\t\n\n\t\t\n\n\t\t\n\t/ ...</code>\".\n\nLINE <em>Line 639, Column 5</em>: \"<code class=\"input\">&lt;script data-senna-track=\"permanent\" id=\"googleAnalyticsScript\" type=\"text/javascript\"&gt;\n\t\t\t\t\t(functi ...</code>\".\n\nLINE <em>Line 952, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\nLiferay.on(\n\t'ddmFieldBlur', function(event) {\n\t\tif (wi ...</code>\".\n\nLINE <em>Line 1052, Column 1</em>: \"<code class=\"input\">&lt;script data-senna-track=\"temporary\" type=\"text/javascript\"&gt;\n\tif (window.Analytics) {\n\t\twindow._com_ ...</code>\".\n\nLINE <em>Line 2142, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n\t(function() {\n\t\tvar select = document.getElementById('_com_liferay_portal_search_web_portl ...</code>\".\n\nLINE <em>Line 2211, Column 2</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\n\n\t\twindow._com_liferay_portal_search_web_portlet_Searc ...</code>\".\n\nLINE <em>Line 2296, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\nAUI().use('liferay-form', function(A) {(function() {var ...</code>\".\n\nLINE <em>Line 3664, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n    if($(\".information-detail__body h2\").length==0){\n        var element=$(\".informacion-ad ...</code>\".\n\nLINE <em>Line 6524, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n    if($(\".information-detail__body h2\").length==0){\n        var element=$(\".informacion-ad ...</code>\".\n\nLINE <em>Line 7522, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n    if($(\".information-detail__body h2\").length==0){\n        var element=$(\".informacion-ad ...</code>\".\n\nLINE <em>Line 8946, Column 1</em>: \"<code class=\"input\">&lt;script&gt;\n    if($(\".information-detail__body h2\").length==0){\n        var element=$(\".informacion-ad ...</code>\".\n\nLINE <em>Line 14063, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\n\n\t\n\t\t\n\n\t\t\t\n\n\t\t\t\n\t\t\n\t\n\n\tLiferay.BrowserSelectors.run();\n ...</code>\".\n\nLINE <em>Line 14092, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n\t// &lt;![CDATA[\n\n\t\t\n\n\t\tLiferay.currentURL = '\\x2fes\\x2fhome';\n\t\tLifera ...</code>\".\n\nLINE <em>Line 14109, Column 2</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n\t\t// &lt;![CDATA[\n\t\t\t\n\t\t\t\t\n\n\t\t\t\t\n\t\t\t\n\t\t// ]]&gt;\n\t\n\n\n\n\n\n\n\n&lt;/script&gt;</code>\".\n\nLINE <em>Line 14140, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\n\n\t\t\t\t\t\t\t\tfunction _com_liferay_asset_publisher_web_por ...</code>\".\n\nLINE <em>Line 14813, Column 1</em>: \"<code class=\"input\">&lt;script src=\"https://www.ehu.eus/o/ehu-theme/js/main.js?browserId=other&amp;amp;minifierType=js&amp;amp;lang ...</code>\".\n\nLINE <em>Line 14818, Column 1</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n\t// &lt;![CDATA[\n\t\tAUI().use(\n\t\t\t'aui-base',\n\t\t\tfunction(A) {\n\t\t\t\tvar f ...</code>\".\n\nLINE <em>Line 14831, Column 10</em>: \"<code class=\"input\">&lt;script type=\"text/javascript\"&gt;\n// &lt;![CDATA[\nLiferay.Loader.require('frontend-js-tooltip-support-web ...</code>\".\n\n"
        }, 
        "WCAG21:link-purpose-in-context": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"Text may refer to items by shape, size, or relative position alone.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 1077, Column 1</em>: \"<code class=\"input\">&lt;body class=\" controls-visible  yui3-skin-sam guest-site signed-out public-page site es_ES\"&gt;\n\n\t&lt;no ...</code>\".\n\n"
        }, 
        "WCAG21:multiple-ways": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"Image may be using color alone.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 4036, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/foroempleo_destacados_.jpg/d399eeb7-ec93-e7b7-3d30 ...</code>\".\n\nLINE <em>Line 4397, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/formacion_profesional_dest.jpg/1def6bda-616d-0b09- ...</code>\".\n\nLINE <em>Line 4758, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/master_egunak_dest_new.jpg/3c37236c-70c1-57d5-e73e ...</code>\".\n\nLINE <em>Line 5119, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/KORRIKA+2022.jpg/79b4122f-389f-304d-4234-abf7a5271 ...</code>\".\n\nLINE <em>Line 5480, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/13743974/Coronavirus.jpg/ec342006-3a76-075d-1b53-00df150654 ...</code>\".\n\nLINE <em>Line 7956, Column 13</em>: \"<code class=\"input\">&lt;img class=\"span4\" alt=' ' src='/documents/10136/0/katagorria_dest.jpg/5af35a0e-77a0-e820-5913-fd042 ...</code>\".\n\n"
        }, 
        "WCAG21:non-text-content": {
          "Resultado": "Failed", 
          "Texto": "The next ERROR was found: \"Image used as anchor is missing valid Alt text.\". You can solve it with: \"\nRepair: Add Alt text that identifies the purpose or function of the image.\n\n           \n           \". The error was in the following line(s): \n\n \"LINE <em>Line 6483, Column 184</em>: \"<code class=\"input\">&lt;img alt=\"\" src=\"https://www.ehu.eus/o/ehu-theme/images/common/rss.png\" style=\"background-image: url ...</code>\"\n\nLINE <em>Line 7481, Column 184</em>: \"<code class=\"input\">&lt;img alt=\"\" src=\"https://www.ehu.eus/o/ehu-theme/images/common/rss.png\" style=\"background-image: url ...</code>\"\n\nLINE <em>Line 8905, Column 148</em>: \"<code class=\"input\">&lt;img alt=\"\" src=\"https://www.ehu.eus/o/ehu-theme/images/common/rss.png\" style=\"background-image: url ...</code>\"\n\n---------------------------------------- \n\n A POTENTIAL PROBLEM was found: \"Alt text does not convey the same information as the image.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 1461, Column 6</em>: \"<code class=\"input\">&lt;img class=\"logo-guest\" src=\"https://www.ehu.eus/o/ehu-theme/images/custom/logo-ucrania.png\" alt=\"UP ...</code>\".\n\n"
        }, 
        "WCAG21:page-titled": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"select element's label is not positioned close to control.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 2062, Column 2</em>: \"<code class=\"input\">&lt;select class=\"form-control search-select\"  id=\"_com_liferay_portal_search_web_portlet_SearchPortlet ...</code>\".\n\n"
        }, 
        "WCAG21:sensory-characteristics": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"img element may require a long description.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 4036, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/foroempleo_destacados_.jpg/d399eeb7-ec93-e7b7-3d30 ...</code>\".\n\nLINE <em>Line 4397, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/formacion_profesional_dest.jpg/1def6bda-616d-0b09- ...</code>\".\n\nLINE <em>Line 4758, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/master_egunak_dest_new.jpg/3c37236c-70c1-57d5-e73e ...</code>\".\n\nLINE <em>Line 5119, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/34166400/KORRIKA+2022.jpg/79b4122f-389f-304d-4234-abf7a5271 ...</code>\".\n\nLINE <em>Line 5480, Column 7</em>: \"<code class=\"input\">&lt;img class=\"span4\" src=\"/documents/10136/13743974/Coronavirus.jpg/ec342006-3a76-075d-1b53-00df150654 ...</code>\".\n\nLINE <em>Line 7956, Column 13</em>: \"<code class=\"input\">&lt;img class=\"span4\" alt=' ' src='/documents/10136/0/katagorria_dest.jpg/5af35a0e-77a0-e820-5913-fd042 ...</code>\".\n\n"
        }, 
        "WCAG21:three-flashes-or-below-threshold": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"Tabular information may be missing table markup.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 1077, Column 1</em>: \"<code class=\"input\">&lt;body class=\" controls-visible  yui3-skin-sam guest-site signed-out public-page site es_ES\"&gt;\n\n\t&lt;no ...</code>\".\n\n"
        }, 
        "WCAG21:use-of-color": {
          "Resultado": "Not checked", 
          "Texto": "A POTENTIAL PROBLEM was found: \"dir attribute may be required to identify changes in text direction.\". The potential problem was in the following line(s): \n\n \"LINE <em>Line 1077, Column 1</em>: \"<code class=\"input\">&lt;body class=\" controls-visible  yui3-skin-sam guest-site signed-out public-page site es_ES\"&gt;\n\n\t&lt;no ...</code>\".\n\n"
        }
      }, 
      "Tester_Name": "Achecker"
    }
    return informe
