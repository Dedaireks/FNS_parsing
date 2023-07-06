import requests
import urllib.parse as parse


def fetch(url, params):
    headers = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8"}
    body = params['body'].encode('utf-8')
    if params['method'] == 'GET':
        return requests.get(url, headers=headers)
    if params['method'] == 'POST':
        return requests.post(url, headers=headers, data=body)


def get_inn(fam, nam, otch, bdate, doctype, docno, docdt):
    docno = str(docno)
    body_params = {
        "c": "find",
        "captcha": "",
        "captchaToken": "",
        "fam": parse.quote_plus(fam),
        "nam": parse.quote_plus(nam),
        "otch": parse.quote_plus(otch),
        "bdate": parse.quote_plus(bdate),
        "doctype": parse.quote_plus(doctype),
        "docno": parse.quote_plus(docno[0:2] + ' ' + docno[2:4] + ' ' + docno[4:]),
        "docdt": parse.quote_plus(docdt)
    }
    inn_request = fetch("https://service.nalog.ru/inn-new-proc.json", {
        "body": parse.urlencode(body_params),
        "method": "POST"
    })
    inn_id = inn_request.json().get('requestId')
    if inn_id:
        inn_response = fetch("https://service.nalog.ru/inn-new-proc.json", {
            "body": "c=get&requestId=" + str(inn_id),
            "method": "POST"
        })
        inn = inn_response.json().get("inn")
        if inn:
            print('ИНН:', inn)
            return {'ИНН': inn}
        else:
            print('Данные не найдены')
            return {'Данные не найдены'}
    else:
        print('Проверьте правильность введенных данных и повторите попытку')
        return {'Проверьте правильность введенных данных и повторите попытку'}


fam = input('Введите фамилию: ')
nam = input('Введите имя: ')
otch = input('Введите отчество: ')
bdate = input('Введите дату рождения: ')
doctype = input(
    'Введите тип документа удостоверяющего личность, 01-Паспорт гражданина СССР, 03-Свидетельство о рождении, 10-Паспорт иностранного гражданина, 12-Вид на жительство в Российской Федерации, \n15-Разрешение на временное проживание в Российской Федерации, 19-Свидетельство о предоставлении временного убежища на территории Российской Федерации, \n21-Паспорт гражданина Российской Федерации, 23-Свидетельство о рождении, выданное уполномоченным органом иностранного государства, 62-Вид на жительство иностранного гражданина: ')
docno = input('Введите серию и номер документа: ')
docdt = input('Введите дату выдачи документа: ')

get_inn(fam, nam, otch, bdate, doctype, docno, docdt)
