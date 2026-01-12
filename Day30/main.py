from bs4 import BeautifulSoup
import requests

#
html_doc = "<html><body><p class='example'>Hello World</p><a href='https://google.com'>Link</a></body></html>"

#
soup = BeautifulSoup(html_doc, 'html.parser')

# NOW your methods will work
element = soup.find("p")
print(element.get_text())
#metoda find
# element = soup.find(name, attrs, recursive, string, **kwargs)

first_link = soup.find("a")

#metoda find_all()
# element = soup.find_all(name, attrs, recursive,string, limit, **kwargs)
all_links = soup.find_all("a")

#metoda select
# elements = soup.select(selector)

example = soup.select('.example')

#metoda get_text
# text = element.get_text(seperator, strip)

text = element.get_text()

#metoda attrs
attributes = element.attrs

# Note: element here refers to the "p" tag found earlier.
# findAll returns a list, so we should use BeautifulSoup instance or a specific tag element that contains links.
# Assuming you want to search within the soup or the existing element.
links = soup.find_all("a")
if links:
    href = links[0].attrs['href']

parent = element.parent
parents = element.parents

parent = element.parent
children = element.children
descendants = element.descendants