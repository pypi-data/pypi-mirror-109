import requests
import hashlib
import time


def bOpen(file):
    f = open(file, "rb")
    content = f.read()
    f.close()

    return content


def boundary():
    seed = str(time.time())
    md5 = hashlib.md5(seed.encode("utf-8"))

    BoundaryHash = "----WebKitFormBoundary" + md5.hexdigest()
    return BoundaryHash


class Instance:
    endpoint = "https://www.labymod.net/api/change/change-texture"
    endpoint_visibility = "https://www.labymod.net/api/change"

    def __init__(self, cookie, itemId):
        self.itemId = itemId
        self.cookies = dict(LABY_SESSION_ID=cookie)
        self.boundary = boundary()

    # -----------------------------------

    def appendBinaryFormData(self, name, payload):
        body = contentType = b""
        eol = b"\r\n"

        disposition = b'name="' + name + b'"'
        if name == b"file":
            contentType = b"Content-Type: image/png" + eol

            filename = str(round(time.time())) + ".png"
            filename = filename.encode()
            disposition += b'; filename="' + filename + b'"'
        body += b"--" + self.boundary.encode() + eol
        body += b"Content-Disposition: form-data; " + disposition + eol
        body += contentType + eol
        body += payload + eol

        self.body += body

    def closeBinaryFormData(self):
        self.body += b"--" + self.boundary.encode() + b"--\r\n\r\n"

    # -----------------------------------

    def addEncodedFormData(self, key, value):
        body = "&"

        if self.body == "":
            body = ""

        body += f"{key}={value}"

        self.body += body

    def update(self, img):
        self.body = b""

        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,sv;q=0.8",
            "cache-control": "no-cache",
            "dnt": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0",
            "origin": "https://www.labymod.net",
            "pragma": "no-cache",
            "referer": "https://www.labymod.net/dashboard",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "Content-Type": "multipart/form-data; boundary=" + self.boundary
        }

        self.appendBinaryFormData(b"cosmetic", b"cape")
        self.appendBinaryFormData(b"file", bOpen(img))

        self.closeBinaryFormData()

        request = requests.post(Instance.endpoint,
                                headers=self.headers,
                                cookies=self.cookies,
                                data=self.body
                                )

        request.raise_for_status()

    def update_visibility(self, value):
        self.body = ""
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,sv;q=0.8",
            "cache-control": "no-cache",
            "dnt": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0",
            "origin": "https://www.labymod.net",
            "pragma": "no-cache",
            "referer": "https://www.labymod.net/dashboard",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        self.addEncodedFormData("type", "switch")
        self.addEncodedFormData("item", self.itemId)
        self.addEncodedFormData("site", "control")

        if type(value) != int:
            if value == "show":
                value = 1
            elif value == "hide":
                value = 0
            else:
                raise ValueError(f"'{value}' is not a valid visibility state.")

        self.addEncodedFormData("value", value)

        request = requests.post(Instance.endpoint_visibility,
                                headers=self.headers,
                                cookies=self.cookies,
                                data=self.body
                                )

        request.raise_for_status()
