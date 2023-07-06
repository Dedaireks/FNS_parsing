import json
import requests
import urllib.parse as parse


def fetch(url, params):
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    if params['body']:
        body = params['body'].encode('utf-8')
    else:
        body = params['body']
    if params['method'] == 'GET':
        return requests.get(url, headers=headers)
    if params['method'] == 'POST':
        return requests.post(url, headers=headers, data=body)


def get_token(query, region, page):
    token = fetch("https://egrul.nalog.ru/", {
        "body": f"vyp3CaptchaToken=&page{page}=&query={parse.quote_plus(query)}&region={region}",
        "method": "POST",
    })
    return token


def get_data(query, region='', page=1):
    results = fetch("https://egrul.nalog.ru/search-result/" +
                    get_token(query, region, page).json()['t'],
                    {
                        "body": None,
                        "method": "GET"
                    })
    if results == {"status: wait"}:
        results = fetch("https://egrul.nalog.ru/search-result/" +
                        get_token(query, region, page).json()['t'],
                        {
                            "body": None,
                            "method": "GET"
                        })
    data = []
    for result in results.json()['rows']:
        item = {}
        if result['k'] == 'ul':
            item['Наименование'] = result['n']
            if result.get('c'):
                item['Сокращенное наименование'] = result['c']
        else:
            item['ФИ'] = result['n']
        if result.get('a'):
            item['Адрес'] = result['a']
        if result.get('i'):
            item['ИНН'] = result['i']
        if result.get('g'):
            item['Должностное лицо'] = result['g']
        if result.get('o'):
            item['ОГРН'] = result['o']
        if result.get('p'):
            item['КПП'] = result['p']
        if result.get('r'):
            item['Дата присвоения ОГРНИП'] = result['r']
        if result.get('e'):
            item['Дата прекращения деятельности'] = result['e']
        if result.get('orn'):
            item['Регистрационный номер, присвоенный до 1 июля 2002 года'] = result['orn']
        data.append(item)

    response = {
        'Количество результатов': results.json()['rows'][0]['tot']
    }
    if int(results.json()['rows'][0]['cnt']) > 10:
        response['Номер страницы'] = results.json()['rows'][0]['pg']
    if int(results.json()['rows'][0]['cnt']) < int(results.json()['rows'][0]['tot']):
        response['Доступно к просмотру'] = results.json()['rows'][0]['cnt']
    response['Результаты'] = data
    return json.dumps(response, indent=4, ensure_ascii=False)


query = input('Введите ИНН или ОГРН (ОГРНИП) или наименование ЮЛ, ФИО ИП: ')
response = get_data(query=query)
print(response)
