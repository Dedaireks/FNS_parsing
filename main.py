import json

import uvicorn as uvicorn
from fastapi import FastAPI
from urllib import parse as parse
from fetch import fetch

app = FastAPI()

with open('IFNS.json') as IFNS:
    IFNS_data = json.load(IFNS)

def get_token(query, region, page):
    token = fetch("https://egrul.nalog.ru/", {
        "body": f"vyp3CaptchaToken=&page{page}=&query={parse.quote_plus(query)}&region={region}",
        "method": "POST",
    })
    return token
@app.get("/get-inn")
def get_inn(fam, nam, otch, bdate, doctype, docno, docdt=''):
    docno = str(docno)
    inn_request = fetch("https://service.nalog.ru/inn-new-proc.json", {
        "body": "c=find&captcha=&captchaToken=&fam=" + parse.quote_plus(fam) + "&nam=" +
                parse.quote_plus(nam) + "&otch=" + parse.quote_plus(
            otch) + "&bdate=" + parse.quote_plus(bdate) + "&doctype=" + parse.quote_plus(
            doctype) + "&docno=" + parse.quote_plus(
            docno[0:2] + ' ' + docno[2:4] + ' ' + docno[4:]) + "&docdt=" + parse.quote_plus(docdt),
        "method": "POST"})
    inn_id = inn_request
    if inn_id.json().get('requestId'):
        inn_id = inn_request.json()['requestId']
        inn_response = fetch("https://service.nalog.ru/inn-new-proc.json", {
            "body": "c=get&requestId=" + str(inn_id),
            "method": "POST"
        })
        inn = inn_response
        if inn.json().get('inn'):
            inn = inn_response.json()["inn"]
            return {'ИНН': inn}
        else:
            return {'Данные не найдены'}
    else:
        return {'Проверьте правильность введённых данных и повторите попытку'}


@app.get("/invalid_inn", description='entity 1 дл поиска по ФЛ, 2 для ЮЛ')
def get_inv_inn_data(query, entity):
    if int(entity) == 1:
        entity = 'fl'
    elif int(entity) == 2:
        entity = 'ul'
    data = fetch("https://service.nalog.ru/invalid-inn-proc.json", {
        "body": f"k={entity}&inn={query}",
        "method": "POST"
    })
    response_data = data.json()
    if response_data.get('date'):
        return {'Дата признания ИНН недействительным': response_data['date']}
    else:
        return {'Информация не найдена'}


@app.get("/foreign_org")
def get_foreign_org_data(kind=2, inn='', kpp='', name='', kio='', pos=1, region=''):
    data = fetch("https://service.nalog.ru/io-proc.do", {
        "body": f"token=&c=search&pos={pos}&SEARCH_KIND={kind}&INN={inn}&KPP={kpp}&NAME={parse.quote_plus(name)}&REGION={region}&ADDR=&KIO={kio}",
        "method": "POST"
    })
    data = data.json()
    if data:
        print('Всего результатов:', data[0]['TOTAL'])
        result = []
        for card in data:
            print('\nИНН:', card['INN'])
            print('КИО:', card['KIO'])
            print('КПП:', card['KPP'])
            if card.get('NAME_S'):
                print('Сокращенное наименование:', card['NAME_S'])
            if card.get('NAME_F'):
                print('Полное наименование:', card['NAME_F'])
            if card.get('NAME_OP_S'):
                print('Сокращенное наименование обособленного подразделения:', card['NAME_OP_S'])
            if card.get('NAME_OP_F'):
                print('Полное наименование обособленного подразделения:', card['NAME_OP_F'])
            if card.get('STATUS'):
                if card['STATUS'] == 1:
                    print('Статус: состоит на учёте')
                else:
                    print('Статус: Снята с учёта')
            print('Налоговый орган постановки на учет:', card['IFNS'], '-', IFNS_data[(card['IFNS'])])
            result.append({
                'ИНН': card['INN'],
                'КИО': card['KIO'],
                'КПП': card['KPP'],
                'Сокращенное наименование': card.get('NAME_S'),
                'Полное наименование': card.get('NAME_F'),
                'Сокращенное наименование обособленного подразделения': card.get('NAME_OP_S'),
                'Полное наименование обособленного подразделения': card.get('NAME_OP_F'),
                'Статус': 'состоит на учете' if card.get('STATUS') == 1 else 'Снята с учета',
                'Налоговый орган постановки на учет': f"{card['IFNS']} - {IFNS_data[card['IFNS']]}",
            })
        return json.dumps(result, ensure_ascii=False)
    else:
        return {'По заданным критериям сведения не найдены'}


@app.get("/egurl_data")
def get_egurl_data(query, region='', page=1):
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
