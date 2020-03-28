import requests
from bs4 import BeautifulSoup

URL = 'http://competiciones.feb.es/estadisticas/Resultados.aspx?g=5&t=2019'

# parse the html and prepare the form
# send post request the form data
page = requests.get(URL)
headers = page.headers
cookies = page.cookies

headers = {
         'Host': 'competiciones.feb.es',
         'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
         'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
         'Accept-Encoding': 'gzip, deflate',
         'Content-Type': 'application/x-www-form-urlencoded',
         'Content-Length': '4437',
         'Origin': 'http://competiciones.feb.es',
         'Connection': 'keep-alive',
         'Referer': 'http://competiciones.feb.es/estadisticas/Resultados.aspx?g=5&t=2019',
         'Upgrade-Insecure-Requests': '1'
}

form={'__EVENTTARGET': 'jornadasDropDownList',
      'jornadasDropDownList': '557539'}

response = requests.post(URL, data=form, headers=headers, cookies=cookies)

new = BeautifulSoup(response.content, 'html.parser')
print(new.prettify())

print('hello world')