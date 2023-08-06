import requests
import requests.auth
import time
import hashlib


def boundary():
    seed = str(time.time())
    md5 = hashlib.md5(seed.encode("utf-8"))

    BoundaryHash = "----WebKitFormBoundary" + md5.hexdigest()
    return BoundaryHash


class LabyAuth:

    def __init__(self, username, password):
        self.session = requests.session()
        self.labyCookie = ""
        self.cookies = dict()
        self.username = username
        self.password = password
        self.boundary = boundary()
        self.body = ""

        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": "Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0",
            "origin": "https://www.labymod.net",
            "pragma": "no-cache",
            "referer": "https://www.labymod.net/de",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-requested-with": "XMLHttpRequest",
            "content-type": "multipart/form-data; boundary=" + self.boundary
        }

        self.appendFormData("memLogin", "false")
        self.appendFormData("rc_key",
                            "03AGdBq262ogkFLac7P1n2slGEyTSPgu0jm-ap7dxU-3jtuWihBM06mBB7B3aLButeDAmO-NX8vvD7-kutDSeq6_pnjXphMEWXorGrcM3Hi0SpnPcVz-9P5sMaennNFkVEapuGmCRBjJBu8oeZi9psdIvr_XJbh1prsPcuAKUNHxHRgZIEikbS4201jNoPghk7dPvHwzE082Xs53-0k3ItgqfTCERFsdoXM6qBVITECBzWkUqKCe5Yma9iFkHBFF65l_9ga6o0B8xi3LRICw8Jhq3cPKxjYTjD671yHCaQW92c0RVNStu5kvj4kX-508rF0ceFdNVLNzsBtnCr_7TsS28HocLLSmM6HYcyJu0SrNhAuFv1xn8ERZaupnXql7ycjw0LkZi1N1u40n6u0ZYkYHnKCnDEmkJbRY4fh_PfES0bnfFMOe3p71Shsd3P2fMPnCx09IidrGv1")
        self.closeFormData()
        self.session.get("https://labymod.net/de")
        self.setCookies()
        self.auth()

    def appendFormData(self, name, payload):
        body = contentType = ""
        eol = "\r\n"

        disposition = 'name="' + name + '"'
        body += "--" + self.boundary + eol
        body += "Content-Disposition: form-data; " + disposition + eol
        body += contentType + eol
        body += payload + eol

        self.body += body

    def closeFormData(self):
        self.body += "--" + self.boundary + "--\r\n\r\n"

    def addEncodedFormData(self, key, value):
        body = "&"

        if self.body == "":
            body = ""

        body += f"{key}={value}"

        self.body += body

    def getCookie(self):
        labyCookie = self.session.cookies.get("LABY_SESSION_ID", domain=".labymod.net")
        return labyCookie

    def auth(self):
        self.cookies = dict(LABY_SESSION_ID=self.getCookie())
        self.session.auth = requests.auth.HTTPBasicAuth(username=self.username, password=self.password)
        res = self.session.post("https://labymod.net/api/auth", cookies=self.cookies, headers=self.headers,
                                data=self.body)
        res.raise_for_status()

    def setCookies(self):
        labyCookie = "sv8u8c3k3323e371g5v53c28si"
        lmLongLive = "35a176a6a605dc88c19c75dc9a86fc9d935b400cb0fdbeb79cc2724f58ff2bccaf4d7dac9aec703b2751470251c64f030d3b024e30baf0c6007415ec18277940"
        lmAcceptCookies = 1
        self.cookies = dict(LABY_SESSION_ID=labyCookie,
                            lm_long_live_token=lmLongLive,
                            lm_accept_cookies=lmAcceptCookies)
        print(self.cookies)
