import requests
import yaml
from urllib.parse import urlencode
from bs4 import BeautifulSoup

from eCharts import ECharts

"""
작성자 : 김준현
작성일 : 20200718
"""
class Cor19:

    def __init__(self):

        self.config    = Cor19.getConfig()
        self.sess      = Cor19.getSessObj()
        self.totalData = list()

    def getCor19Information(self):

        try:

            html = self.sess.get(self.urlReturn())
        except requests.exceptions.ConnectionError as err:
            print(err)
        else:
            bsObj = BeautifulSoup(html.text, "html.parser")
            ppcUXd = bsObj.select_one("tbody.ppcUXd").select("tr.sgXwHf.wdLSAe.YvL7re")
            for p in ppcUXd:

                national      = p.select_one("th.l3HOY > div.TWa0lb > div.pcAJd")
                tdInformation = [ i for i in p.select("td.l3HOY") ]

                elements = [None for _ in range(4)]
                for c, i in enumerate([0, 2, 3, 4]):
                    if tdInformation[i].string != "데이터 없음":
                        elements[c] = int(str(tdInformation[i].string).replace(",", ""))
                    else:
                        elements[c] = "데이터 없음"

                self.totalData.append({
                    "national" : national.string,
                    "confirmer": elements[0],
                    "confir_num_per_million": elements[1],
                    "cure": elements[2],
                    "die" : elements[3]
                })

        finally:
            self.sess.close()

    def urlReturn(self):
        """
        :return: requests url
        """
        params = urlencode({
            "hl"  : "ko",
            "mid" : "/m/02j71",
            "gl"  : "KR",
            "ceid": "KR:ko"
        })
        url = self.config["url"] +"?"+  params
        return url

    @classmethod
    def getSessObj(cls):
        """
        :return: requests.Session
        """
        sess= requests.Session()
        return sess

    @classmethod
    def getConfig(cls):
        """
        :return: yaml file
        """
        try:
            f=open("./config/urlinfo.yml", "r", encoding="utf-8")
        except FileNotFoundError as err:
            print(err)
            exit(1)
        else:
            information = yaml.safe_load(f)
            f.close()
            return information

if __name__ == "__main__":
    o = Cor19()
    o.getCor19Information()
    ECharts.barGraph(datas=o.totalData)