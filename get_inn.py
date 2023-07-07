import urllib.parse as parse
from fetch import fetch


def get_inn(fam, nam, otch, bdate, doctype, docno, docdt):
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
            print('ИНН:', inn)
            return {'ИНН': inn}
        else:
            print('Данные не найдены')
            return {'Данные не найдены'}
    else:
        print('Проверьте правильность введённых данных и повторите попытку')
        return {'Проверьте правильность введённых данных и повторите попытку'}


get_inn(input('Введите фамилию: '), input('Введите имя: '), input('Введите отчество: '),
        input('Введите дату рождения: '), input(
        'Введите тип документа удостоверяющего личность, 01-Паспорт гражданина СССР, 03-Свидетельство о рождении, 10-Паспорт иностранного гражданина, 12-Вид на жительство в Российской Федерации, \n15-Разрешение на временное проживание в Российской Федерации, 19-Свидетельство о предоставлении временного убежища на территории Российской Федерации, \n21-Паспорт гражданина Российской Федерации, 23-Свидетельство о рождении, выданное уполномоченным органом иностранного государства, 62-Вид на жительство иностранного гражданина: '),
        input('Введите серию и номер документа : '), input('Введите дату выдачи документа: '))
