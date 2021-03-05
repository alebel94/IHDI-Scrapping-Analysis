from bs4 import BeautifulSoup
import requests
import pprint
page = requests.get('https://en.wikipedia.org/wiki/Gross_domestic_product.html')

soup = BeautifulSoup(page.content, 'html.parser')
pretty_soup = soup.prettify()

soup_element_list = [type(item) for item in list(soup.children)]

html = list(soup.children)[2]
html_element_list = [type(item) for item in list(html.children)]
print( html.index(html))
