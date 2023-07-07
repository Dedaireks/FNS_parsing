from fetch import fetch
from urllib import parse as parse
import json


def get_data(query, page=1, pagesize=25):
    data = fetch("https://service.nalog.ru/disqualified-proc.json", {
        "body": f"page={page}&pagesize={pagesize}&query={parse.quote_plus(query)}",
        "method": "POST"
    })
    data = data.json()
    if data['data']:
        result = []
        for card in data['data']:
            result.append({
                'Номер записи РДЛ': card['НомЗап'],
                'Дисквалифицированное лицо': card['ФИО'],
                'Дата рождения': card['ДатаРожд'],
                'Место рождения': card.get('МестоРожд'),
                'Организация': card['НаимОрг'],
                'ИНН организации': card.get('ИННОрг'),
                'Должность': card['Должность'],
                'Статья КоАП РФ': card['КвалификацияТекст'],
                'Наименование органа, составившего протокол': card['НаимОргПрот'],
                'Судья': card['ФИОСуд'],
                'Должность судьи': card['ДолжностьСуд'],
                'Срок дисквалификации': card['ДисквСрок'],
                'Дата начала': card['ДатаНачДискв'],
                'Дата конца': card['ДатаКонДискв']
            })
        return json.dumps(result, indent=4, ensure_ascii=False)
    else:
        return 'Сведения не найдены.'


query = input('Введите ФИО ФЛ, наименование или ИНН ЮЛ: ')
response = get_data(query=query)
print(response)
