import requests
from bs4 import BeautifulSoup

def searchWiki(query, limit=5):
    S = requests.Session()
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'utf8': '',
        'format': 'json',
        'srlimit': limit,
    }

    resp = S.get('https://ru.wikipedia.org/w/api.php', params=params)
    data = resp.json().get('query', {}).get('search', [])
    result = []
    for item in data:
        pageid = item['pageid']
        title = item['title']
        page = S.get('https://ru.wikipedia.org/w/api.php', params={
            'action': 'parse',
            'pageid': pageid,
            'prop': 'text',
            'format': 'json'
        }).json()
        html = page.get('parse', {}).get('text', {}).get('*', '')
        soup = BeautifulSoup(html, 'html.parser')
        p=soup.find('p')
        summary = p.get_text().strip if p else ''

        info = soup.find('table', {'class': 'infobox'})
        year = None
        genre = ''
        author = ''
        if info:
            for row in info.find_all('tr'):
                th=row.find('th')
                td=row.find('td')
                if not th or not td:
                    continue
                key = th.get_text().lower()
                val = td.get_text().strip()
                if 'год' in key:
                    try:
                        year=int(val.strip()[:4])
                    except:
                        pass
                elif 'жанр' in key:
                    genre=val
                elif 'автор' in key:
                    author=val
        result.append({
            'external_id': f"wikipedia-{pageid}",
            'title': title,
            'aithor': author,
            'year': year,
            'genre': genre,
            'summary': summary,
        })
    return result

def search_litres(query, limit=5):
    """
    Заглушка: аналогично можно реализовать через парсинг HTML litres.ru
    """
    # TODO: расширить под реальный парсинг LitRes
    return []