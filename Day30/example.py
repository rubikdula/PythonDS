from bs4 import BeautifulSoup


def get_page_content(url):
    response = requests.get(url, headers)
    if response.status_code = 200:
        return response.text
    return None

#funksioni qe na mundeson ekstraktimin e te dhenave nga faqja e internetit
def extract_Articles(content):
    soup = BeautifulSoup(content, 'html.parser')
    articles =[]

    for article in soup.find_all('div', class_='search-item'):
        title_div = article.find('div', class_='search-txt')
        title='No title found'
        link='No link found'
        date='No date found'
        description='No description found'

        if title_div:
            title_tag = title_div.find('a')
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag['href']

            meta_ul = title_div.find('ul', class_='story-meta')
            if meta_ul:
                date_li = meta_ul.find('li')[0]
                if date_li:
                    date = date_li.get_text(strip=True)

            description_tag = article.find('p')
            if description_tag:
                description = description_tag.get_text(strip=True)

        articles.append({'title': title, 'link': link, 'date': date, 'description': description})

    return articles