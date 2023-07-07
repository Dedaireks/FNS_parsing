import requests
from fetch import fetch


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
        print('Дата признания ИНН недействительным:', response_data['date'])
        return {'Дата признания ИНН недействительным': response_data['date']}
    else:
        print('Информация не найдена')
        return {'Информация не найдена'}


entity_type = input('Введите тип запроса, 1 для поиска ФЛ, 2 для поиска ЮЛ: ')
inn = input('Введите недействительный ИНН: ')
print(get_data(inn, entity_type))
