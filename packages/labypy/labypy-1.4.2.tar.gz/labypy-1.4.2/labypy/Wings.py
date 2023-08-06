import requests


class Instance:
    endpoint = "https://www.labymod.net/api/change"
    endpoint_visibility = "https://www.labymod.net/api/change"

    def __init__(self, cookie, itemId):
        self.itemId = itemId
        self.cookies = dict(LABY_SESSION_ID=cookie)

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

        self.body = ""

        # Payload
        self.addEncodedFormData("item", itemId)
        self.addEncodedFormData("site", "control")

    # -----------------------------------

    def addEncodedFormData(self, key, value):
        body = "&"

        if self.body == "":
            body = ""

        body += f"{key}={value}"

        self.body += body

    # -----------------------------------

    def update(self, value):

        self.addEncodedFormData("type", "multi")
        self.addEncodedFormData("value", value)

        try:
            res = requests.post(Instance.endpoint,
                                headers=self.headers,
                                cookies=self.cookies,
                                data=self.body
                                )
            res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 429:
                print("Too many requests! Waiting a bit...")
                time.sleep(5)
                res = requests.post(Instance.endpoint,
                                    headers=self.headers,
                                    cookies=self.cookies,
                                    data=self.body
                                    )
                res.raise_for_status()
            if err.response.status_code == 400:
                return print("You tried to send something bad fuck you!")
            if err.response.status_code == 403:
                return print("You need to change the Labymod cookie!")

    def update_visibility(self, value):
        if type(value) != int:
            if value == "show":
                value = 1
            else:
                value = 0

        self.addEncodedFormData("type", "switch")
        self.addEncodedFormData("value", value)

        request = requests.post(Instance.endpoint_visibility,
                                headers=self.headers,
                                cookies=self.cookies,
                                data=self.body
                                )

        request.raise_for_status()
