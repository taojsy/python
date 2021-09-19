import requests
from bs4 import BeautifulSoup


def pronto_status(pronto_id):
	url = 'https://pronto.int.net.nokia.com/pronto/problemReportSearch.html?freeTextdropDownID=prId&searchTopText=' + pronto_id
	req = requests.get(url)
	web_content = BeautifulSoup(req.text, 'lxml')
	web_content = web_content.find('div',{"class" : 'My(6px) Pos(r) smartphone_Mt(6px)'})
	web_content = web_content.find('span').text

	return web_content