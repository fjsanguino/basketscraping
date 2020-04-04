import requests
from bs4 import BeautifulSoup

URL = 'http://competiciones.feb.es/estadisticas/Resultados.aspx?g=5&t=2019'

# parse the html and prepare the form
# send post request the form data


response = requests.post(URL, data=form, headers=headers, cookies=cookies)

new = BeautifulSoup(response.content, 'html.parser')
print(new.prettify())

print('hello world')

mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="g3GJdRGWE4",
    passwd="4I1ZMfcMXg",
    database="g3GJdRGWE4"
)

query = "select * from stats where true"

queries_pd = pd.read_sql(query, con=mydb)