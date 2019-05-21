import urllib.request
import json
from pathlib import Path
import sys
from .setting import TURING_ID_FILE, TURING_KEY_FILE

class Request:

    def __init__(self, url, method=None, data=None, headers=None, encoding='utf-8', expect_json=False):
        self.url = url
        self.method = method
        self.data = data
        self.headers = headers or {}
        self.encoding = encoding
        self.expect_json = expect_json

    def send(self):
        http_post = urllib.request.Request(self.url, data=self.data, headers=self.headers, method=self.method)
        response = urllib.request.urlopen(http_post)
        response_str = response.read().decode(self.encoding)
        if self.expect_json:
            response_dic = json.loads(response_str)
            return response_dic
        return response_str

    @classmethod
    def read_file(cls, file):
        f = Path(file)
        if f.is_file():
            return f.read_text()
        else:
            raise FileNotFoundError('Credential file not found at {}'.format(f))


class TuringRequest(Request):
    api_url = "http://openapi.tuling123.com/openapi/api/v2"
    api_id = ''
    api_key = ''

    def __init__(self, msg):
        if not self.has_credential():
            self.init_credential()
        self._headers = {'content-type': 'application/json'}
        self._msg = msg
        self._info = {
            "perception":
            {
                "inputText":
                {
                    "text": self._msg
                },

                "selfInfo":
                {
                    "location":
                    {
                        "city": "北京",
                        "province": "北京",
                        "street": "清华路"
                    }
                }
            },
            "userInfo":
            {
                "apiKey": self.api_key,
                "userId": self.api_id
            }
        }
        self._data = json.dumps(self._info).encode('utf-8')
        return super().__init__(self.api_url,
                                method='POST',
                                data=self._data,
                                headers=self._headers,
                                encoding='utf-8',
                                expect_json=True)
    
    def send(self):
        rt = super().send()
        return rt['results'][0]['values']['text']

    @classmethod
    def init_credential(cls):
        cls.dir = (Path.cwd()/sys.argv[0]).parent
        f1 = cls.dir / TURING_ID_FILE
        f2 = cls.dir / TURING_KEY_FILE
        cls.api_id = cls.read_file(f1)
        cls.api_key = cls.read_file(f2)

    @classmethod
    def has_credential(cls):
        return cls.api_id and cls.api_key


if __name__ == "__main__":
    TuringRequest.init_credential()
    print(TuringRequest.api_id)
    print(TuringRequest.api_key)
