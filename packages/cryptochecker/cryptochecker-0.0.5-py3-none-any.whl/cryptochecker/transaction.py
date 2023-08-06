import requests
from selectorlib import Extractor

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
'Accept-Encoding': 'gzip, deflate, br',
'Connection': 'keep-alive'}

btc_string = """
addresses_from:
    css: 'div.ge5wha-0 > a.sc-1r996ns-0'
    xpath: null
    multiple: true
    type: Text
addresses_to:
    css: 'div.sc-19pxzmk-0 a.sc-1r996ns-0'
    xpath: null
    multiple: true
    type: Text
status_n:
    css: 'div.sc-8sty72-0 div span.sc-1ryi78w-0.sc-1yunmav-0'
    xpath: null
    type: Text
status_p:
    css: 'div.sc-8sty72-0 span.sc-1ryi78w-0.sc-45ldg2-0'
    xpath: null
    type: Text
total_input:
    css: 'div.sc-1enh6xt-0:nth-of-type(8) span.sc-1ryi78w-0.u3ufsr-0'
    xpath: null
    type: Text
total_output:
    css: 'div.sc-1enh6xt-0:nth-of-type(9) span.sc-1ryi78w-0.u3ufsr-0'
    xpath: null
    type: Text
fee_amount:
    css: 'div.sc-1enh6xt-0:nth-of-type(10) span.sc-1ryi78w-0.u3ufsr-0'
    xpath: null
    type: Text
"""

eth_string = """
addresses_from:
    css: 'div.ccso3i-0 > a.sc-1r996ns-0'
    xpath: null
    multiple: true
    type: Text
addresses_to:
    css: div.sc-1rk8jst-2
    xpath: null
    multiple: true
    type: Text
status_n:
    css: 'div.sc-8sty72-0 div span.sc-1ryi78w-0.sc-1yunmav-0'
    xpath: null
    type: Text
status_p:
    css: span.sc-1ryi78w-0.sc-45ldg2-0
    xpath: null
    type: Text
t_input:
    css: 'div.sc-1enh6xt-0:nth-of-type(5) span.sc-1ryi78w-0.u3ufsr-0'
    xpath: null
    type: Text
t_output:
    css: 'div.sc-1enh6xt-0:nth-of-type(9) span.sc-1ryi78w-0.u3ufsr-0'
    xpath: null
    type: Text
fee_amount:
    css: 'div.sc-1enh6xt-0:nth-of-type(7) span.sc-1ryi78w-0.u3ufsr-0'
    xpath: null
    type: Text
"""

class cleanUp:
    def __init__(self, **transaction):
        self.__dict__.update(transaction)

class non_access:
    
    def status(info):
        if info['status_p'] == None:
            info.pop('status_p',None)
            info['status'] = info['status_n']
            info.pop('status_n',None)
        else:
            info.pop('status_n',None)
            info['status'] = info['status_p']
            info.pop('status_p',None)
        return info


    def make_request(crypto,tx):
        line = '======================================='
        if crypto not in ['btc','eth']:
            print(f"{line}\nWrong crypto name specified!\n{line}")
            return False
        with requests.session() as s:
            page = s.get(url=f"https://www.blockchain.com/{crypto}/tx/{tx}",headers = headers)  
        if page.status_code != 200:
            print(f'{line}\nCannot connect to blockchain.com\nStatus Code: {page.status_code}\n{line}')
            return False
        if crypto == 'btc':
            c = btc_string
        else:
            c=eth_string
        e = Extractor.from_yaml_string(c)
        info = e.extract(page.text)
        return non_access.status(info)


def check(crypto,tx,clean=None):
    crypto,tx = crypto.lower(),tx.lower()
    response = non_access.make_request(crypto,tx)
    if response != False and clean == True:
        transaction_object = cleanUp(**response)
        return transaction_object
    else:return response
