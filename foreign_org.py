import requests
import urllib.parse as parse
import json


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


with open('IFNS.json') as IFNS:
    IFNS_data = json.load(IFNS)


def get_data(kind=2, inn='', kpp='', name='', kio='', pos=1, region=''):
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
        return json.dumps(result, indent=4, ensure_ascii=False)
    else:
        print('По заданным критериям сведения не найдены')
        return {'По заданным критериям сведения не найдены'}


inn, kpp, reg, kio, name, kind = '', '', '', '', '', ''
kind = input("Введите тип поиска (1-3):\n1 - ИНН/КПП\n2 - Наименование\n3 - КИО\n")

if kind == '1':
    inn = (input("Введите ИНН: "))
    kpp = (input("Введите КПП: "))
    reg = (input("Введите номер региона, оставьте пустым для поиска по всем регионам: : "))
elif kind == '2':
    name = input("Введите наименование иностранной организации/обособленного подразделения: ")
    reg = input("Введите номер региона, оставьте пустым для поиска по всем регионам: : ")
elif kind == '3':
    kind = '4'
    kio = input("Введите КИО: ")
response = get_data(kind=kind, inn=inn, kpp=kpp, name=name, kio=kio)
print(response)
