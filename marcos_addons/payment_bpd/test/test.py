from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests import Request, Session
import json
import ssl
import requests
from pprint import pprint as pp

CERT = "/Users/eneldoserrata/PycharmProjects/bitbucket/marcos_odoo/marcos_addons/payment_bpd/test/cartone.pem"
URL = "https://pruebas.azul.com.do/Webservices/JSON/default.aspx"

tarjetas = {"visa_aprove": "4012000077777777",
            "visa_decline": "4012000088888886",
            "mastercard_aprove": "5424180279791773",
            "mastercard_decline": "5424180279791740",
            "discover_aprove": "6011000991200035",
            "discover_aprove": "6011000990099826"}

tx_bpd_request = {"Channel": "EC",
                  "Store": "39040200107",
                  "CardNumber": tarjetas["visa_aprove"],
                  "Expiration": "201512",
                  "CVC": "123",
                  "PosInputMode": "E-Commerce",
                  "TrxType": "Sale",
                  "Amount": "650730",
                  "Itbis": "99264",
                  "CurrencyPosCode": "$",
                  "Payments": "1",
                  "Plan": "0",
                  "AcquirerRefData": "1",
                  "RRN": "null",
                  "CustomerServicePhone": "809-111-2222",
                  "OrderNumber": "234",
                  "ECommerceUrl": "www.miurl.com.do",
                  "CustomOrderId": "ABC123"
                  }
headers = {"Content-Type": u"application/json",
           "Auth1": u"cartone",
           "Auth2": u"cartone"}


class Ssl3HttpAdapter(HTTPAdapter):
    """"Transport adapter" that allows us to use SSLv3."""

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1_2)


s = requests.Session()
s.mount(URL, Ssl3HttpAdapter())

req = Request("POST", URL, data=json.dumps(tx_bpd_request), headers=headers)
prepped = s.prepare_request(req)


res = s.send(prepped, cert=CERT)
# res = requests.post(URL, json=json.dumps(tx_bpd_request), headers=headers, verify=CERT)
print res.text