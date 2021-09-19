# import requests, sys, webbrowser, bs4
#
#
# url=r'https://pronto.int.net.nokia.com/pronto/problemReport.html?prid=PR586576'
# res=requests.get(url,auth=('horao', 'Hop'))
#
# #res=requests.get(url)
# # try:
# # 	res.raise_for_status()
# # except Exception as e:
# # 	print("enter pronto page failed: id={},reason={}".format(pronto_id,str(e)))
# content = bs4.BeautifulSoup(res.text,features="lxml")
# #content = res.json()
# print(content)

import requests

def get_pronto_info(pronto_id):
    #prefix=r'/problemReport/{}'.format(pronto_id)
    #url="{}{}".format(base_url,prefix)
    url=r'https://pronto.int.net.nokia.com/prontoapi/rest/api/1/problemReport/{}'.format(pronto_id)
    #url=r'https://pronto.int.net.nokia.com/prontoapi/rest/api/latest/problemReport?startAt=0&maxResults=25'
#   res=requests.get(url,auth=('horao', 'Hop!1234'))
    res=requests.get(url,auth=('jutao', 'xxx'))
    return res.text

res=get_pronto_info("PR561005")
print(res)