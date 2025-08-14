import aiohttp
from bs4 import BeautifulSoup


url = 'https://ru.investing.com/economic-calendar/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0'
}

async def get_current_news():
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            page = await response.text()
            
            soup = BeautifulSoup(page, 'html.parser')
            
            table = soup.find('table', {'id': 'economicCalendarData'})
            
            elements = table.find_all('tr', class_='js-event-item')

            parsed_data: list[dict] = []
            
            
            for el in elements[-15:]:
                el_id = el.get('id').split('_')[-1]
                time = el.find('td', class_='first left time js-time').text
                currency = el.find('td', class_='left flagCur noWrap').text
                title = el.find('a', target='_blank').text.strip()
                forecast = el.find('td', id=f'eventForecast_{el_id}')

                forecast = forecast.text if forecast.text.strip() != '' else 'Не обнаружено'
                
                before = el.find('td', id=f'eventPrevious_{el_id}').text
                
                parsed_data.append({'time':time, 'currency':currency, 'title':title, 'forecast':forecast, 'before':before})
            return parsed_data