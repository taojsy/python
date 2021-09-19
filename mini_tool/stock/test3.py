import requests


def get_pronto_info(pronto_id):
    url=r'https://pronto.int.net.nokia.com/prontoapi/rest/api/latest/problemReport/{}'.format(pronto_id)
    para={
        "startAt": 0,
        "maxResults": 300
    }
    res=requests.get(url,params=para, auth=('horao', 'Hop!1234'))
    return res.json()


def get_pronto_view(view_id, viewState="Open"):
    url=r'https://pronto.int.net.nokia.com/prontoapi/rest/api/latest/view/{}/viewResult'.format(view_id)
    para={
        "viewState":viewState,
        "startAt": 0,
        "maxResults": 5000
    }
    res=requests.get(url,params=para, auth=('horao', 'Hop!1234'))
    return res.json()


res=get_pronto_view("VIEW872447")
print(res)
print(len(res['values']))
open_pronts=[i for i in res['values'] if i["state"]!="Closed" and i["state"]!="Correction Not Needed"]
print(len(open_pronts))
for i in open_pronts:
    print(i)