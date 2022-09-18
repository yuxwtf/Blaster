import os
import sys
import requests
import random
import string
import pystyle
import threading
import re


blaster = """

▄▄▄▄· ▄▄▌   ▄▄▄· .▄▄ · ▄▄▄▄▄▄▄▄ .▄▄▄  
▐█ ▀█▪██•  ▐█ ▀█ ▐█ ▀. •██  ▀▄.▀·▀▄ █·
▐█▀▀█▄██▪  ▄█▀▀█ ▄▀▀▀█▄ ▐█.▪▐▀▀▪▄▐▀▀▄ 
██▄▪▐█▐█▌▐▌▐█ ▪▐▌▐█▄▪▐█ ▐█▌·▐█▄▄▌▐█•█▌
·▀▀▀▀ .▀▀▀  ▀  ▀  ▀▀▀▀  ▀▀▀  ▀▀▀ .▀  ▀

"""


class Exploits:

    def __init__(self, url_):
        self.url = url_
        self.exploit_nb = 0
        self.sfile_nb = 0
        self.payload = "database"
        self.xss_nb = 0

    def xss(self):
        criticlvl = 3
        r = requests.get('http://web.archive.org/cdx/search/cdx?url=*.{}&output=text&fl=original&collapse=urlkey'.format(self.url))
        for exploit in str(r.text).splitlines():
            if self.payload in exploit:
                self.xss_nb = self.xss_nb + 1
                print(pystyle.Colors.green, pystyle.Center.XCenter(f'(+) Found: {exploit} [StatusCode: {str(r.status_code)}] [CriticLevel: {criticlvl}]'), pystyle.Colors.white)
            else:
                print(pystyle.Colors.red, pystyle.Center.XCenter(f'(-) Found: {exploit} [StatusCode: {str(r.status_code)}] [CriticLevel: 0]'), pystyle.Colors.white)

    def secretfiles(self):
        criticlvl = 1
        communsfile = ['web.config', 'config', 'logs.txt', 'admin.txt', 'log.txt', 'pass.txt', 'content.txt', 'admin.config', 'logs', 'log', 'administator', 'passwords', 'databases', 'db.json', 'database.sql', 'db.sql', 'data.sql']
        for file in communsfile:
            url_ = f"http://{self.url}/{file}"
            r = requests.get(str(url_))
            if r.status_code == 200:
                self.sfile_nb = self.sfile_nb + 1
                print(pystyle.Colors.green, pystyle.Center.XCenter(f'(+) Found: {url_} [StatusCode: {str(r.status_code)}] [CriticLevel: {criticlvl}]'), pystyle.Colors.white)
            else:
                print(pystyle.Colors.red, pystyle.Center.XCenter(f'(-) Unable To Found: {url_} [StatusCode: {str(r.status_code)}] [CriticLevel: 0]'), pystyle.Colors.white)

    def reverseIP(self):
        requ = requests.get("https://api.hackertarget.com/reverseiplookup/?q="+self.url)
        resp = requ.text
        output = resp
        for lines in str(output).splitlines():
            print(pystyle.Colors.green, pystyle.Center.XCenter(f'(+) {lines}'), pystyle.Colors.white)

    def httpHeader(self):
        requ = requests.get("https://api.hackertarget.com/httpheaders/?q="+self.url)
        resp = requ.text
        output = resp.strip().lstrip()
        for lines in str(output).splitlines():
            print(pystyle.Colors.green, pystyle.Center.XCenter(f'(+) {lines}'), pystyle.Colors.white)

    def TcpPort(self):
        requ = requests.get("https://api.hackertarget.com/nmap/?q="+self.url)
        resp = requ.text
        output = resp.strip().lstrip()
        for lines in str(output).splitlines():
            print(pystyle.Colors.green, pystyle.Center.XCenter(f'(+) {lines}'), pystyle.Colors.white)

    def ExtractPagesLinks(self):
        requ = requests.get("https://api.hackertarget.com/pagelinks/?q="+self.url)
        resp = requ.text
        output = resp.strip().lstrip()
        for lines in str(output).splitlines():
            print(pystyle.Colors.green, pystyle.Center.XCenter(f'(+) {lines}'), pystyle.Colors.white)

    def IpLocation(self):
        requ = requests.get("https://api.hackertarget.com/geoip/?q="+self.url)
        resp = requ.text
        output = resp.strip().lstrip()
        for lines in str(output).splitlines():
            print(pystyle.Colors.green, pystyle.Center.XCenter(f'(+) {lines}'), pystyle.Colors.white)

    def ports(self):
        requ = requests.post("https://www.portcheckers.com/portscan-result", data={'server': self.url, "quick": "false"})
        resp = requ.text
        print(resp)
        output = re.sub('<pre>|\t|</pre>|<div style="margin:10px 0 20px 0;"><h3>Port Scan Result</h3>|'
                        '<span style="display: inline-block;width:200px;">|</span><span class="label label-danger">|</span>'
                        '|<span class="label label-success">|', '', resp).strip().lstrip()

        output = output.replace("Not Available", " Not Available")
        for lines in str(output).splitlines():
            print(pystyle.Colors.green, pystyle.Center.XCenter(f'(+) {lines}'), pystyle.Colors.white)

    def sql(self):
        criticlvl = 3
        files = ['index', 'search', 'contacts', 'home', 'main', 'catalog', 'items', 'logs', 'log', 'endpoint']
        items = ['user', 'item', 'contact', 'item', 'page', 'tab', 'type']
        for file in files:
            for item in items:
                url_ = "http://" + str(self.url) + "/" + str(file) + ".php?" + str(item) + "=1'"
                r = requests.get(str(url_))
                if r.status_code == 200:
                    if "sql" in str(r.content):
                        self.exploit_nb = self.exploit_nb + 1
                        print(pystyle.Colors.green, pystyle.Center.XCenter(f'(+) Found: {url_} [StatusCode: {str(r.status_code)}] [CriticLevel: {criticlvl}]'), pystyle.Colors.white)
                    else:
                        print(pystyle.Colors.orange, pystyle.Center.XCenter(f'(+) Found: {url_} [StatusCode: {str(r.status_code)}] [CriticLevel: 0]'), pystyle.Colors.white)
                else:
                    print(pystyle.Colors.red, pystyle.Center.XCenter(f'(-) Unable To Found: {url_} [StatusCode: {str(r.status_code)}] [CriticLevel: 0]'), pystyle.Colors.white)
def main():
    os.system('cls')
    print(pystyle.Colorate.Horizontal(pystyle.Colors.blue_to_cyan, pystyle.Center.XCenter(blaster), 2))
    print('\n\n')
    targeturl = pystyle.Write.Input("\n     (>) Target Url: ", pystyle.Colors.yellow, interval=0.0025)
    print(pystyle.Colors.yellow, f'\n     (*) Scanning Website...', pystyle.Colors.white)
    exploiters = Exploits(str(targeturl))
    print(pystyle.Colors.orange, pystyle.Center.XCenter(f'\n\n ------------- XSS ------------- \n\n'), pystyle.Colors.white)
    exploiters.xss()
    print(pystyle.Colors.yellow, pystyle.Center.XCenter(f'\n\n ------------- FOUND {str(exploiters.xss_nb)} XSS EXPLOIT ------------- \n\n'), pystyle.Colors.white)
    print(pystyle.Colors.orange, pystyle.Center.XCenter(f'\n\n ------------- SQL ------------- \n\n'), pystyle.Colors.white)
    exploiters.sql()
    print(pystyle.Colors.yellow, pystyle.Center.XCenter(f'\n\n ------------- FOUND {str(exploiters.exploit_nb)} SQL EXPLOIT ------------- \n\n'), pystyle.Colors.white)
    print(pystyle.Colors.orange, pystyle.Center.XCenter(f'\n\n ------------- Secret-Files ------------- \n\n'), pystyle.Colors.white)
    exploiters.secretfiles()
    print(pystyle.Colors.yellow, pystyle.Center.XCenter(f'\n\n ------------- FOUND {str(exploiters.sfile_nb)} FILES ------------- \n\n'), pystyle.Colors.white)
    print(pystyle.Colors.orange, pystyle.Center.XCenter(f'\n\n ------------- Server-Info ------------- \n\n'), pystyle.Colors.white)
    exploiters.IpLocation()
    print(pystyle.Colors.orange, pystyle.Center.XCenter(f'\n\n ------------- Page-Links ------------- \n\n'), pystyle.Colors.white)
    exploiters.ExtractPagesLinks()
    print(pystyle.Colors.orange, pystyle.Center.XCenter(f'\n\n ------------- TCP-Port ------------- \n\n'), pystyle.Colors.white)
    exploiters.TcpPort()
    print(pystyle.Colors.orange, pystyle.Center.XCenter(f'\n\n ------------- HTTP-Headers ------------- \n\n'), pystyle.Colors.white)
    exploiters.httpHeader()
    print(pystyle.Colors.orange, pystyle.Center.XCenter(f'\n\n ------------- Reverse-IP ------------- \n\n'), pystyle.Colors.white)
    exploiters.reverseIP()

if __name__ == "__main__":

    main()