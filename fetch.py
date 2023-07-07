import requests


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



