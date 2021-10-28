import requests

headers = {
    'authority': 'map.naver.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'accept-language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'content-type': 'application/json',
    'accept': 'application/json, text/plain, */*',
    'expires': 'Sat, 01 Jan 2000 00:00:00 GMT',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://map.naver.com/',
    'cookie': 'NNB=YYF7WTTONT7GA; NID_AUT=6XDDHNp+RcKAoZR4X6WEGoEfGvfj/yinwhkuRt1FzzhwIWk1O2ghLoG+HBCOEkOf; NID_JKL=CcQOovGLIQDJuVb+/+nCI5UhKmVJKR84vJlqN/fIt9o=; _ga=GA1.2.878040348.1627623526; ASID=dc5f3dbd0000017bc9a08e5f0000005a; nx_ssl=2; NV_WETR_LOCATION_RGN_M="MDUyMDA2MjQ="; NV_WETR_LAST_ACCESS_RGN_M="MDUyMDA2MjQ="; m_loc=568796a9a798b031c79ce34c474a916b745a603ef49a3efae027330981851c165c45d208eb010b902a04b8027ba06bef; NFS=2; MM_NEW=1; BMR=s=1635143616649&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.naver%3FisHttpsRedirect%3Dtrue%26blogId%3Dmck0903%26logNo%3D221442957432&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=hUB9Uwp0Jywss57kc14ssssssGs-143163; NID_SES=AAABoy5ozN6EJExAUonEShMqVsREzJTLj7kjDOxSTAwEydvmtlRHm1KHvlBWYFPC+Xj8KmcoTtTafkUhRtSTsWIHOsXwEMF1iFSqVbfV4K8VDSaLazvIMf68htjYPDVPBFlfjaSWNM2J5V1JuUNZcQLqFe7RYnxDL68A6u2GcqkMe6JnmHX3VK1MBRzyXAlbE5PnfqDdbl6E1Qrs3tElulrLI+j14DVVv7jXX3SxbMumsRySoXqOcAc33z9TDLA611V55NG7j3wxvNzXa5flXbzySN2EscMBr76W7hoIgxYK+uyBiFGj0zSy3wv5ZRXynTLCAiE/+V+FkzvqqF/ADjZNKlxQxHSVLWEfJgYYpXpKyGk4TxllawworPoJyzM4nzFL9KhH1ZWH/Y7UjOcb1m1col/HfWbhmwTONxNcsIWu4rPtqlQh2v78M8YO68HkDcWGgjk8wxDtRUmz/oUHeOu6PGQlYfcgCP0ps/dWO2aoKgQAJep4K1SO3oiDsMCwk4diBwNUo9FSzTjT8TRq73/vHxPyHl3SZp4yOaPF3t4abVxPqmZW6UPB92/2DmEAtpgV5Q==; csrf_token=1929a7a5a62b1e0001d7b63e976c8ae2c775ca6ca9ee0a51f671bfc170779510819d3335dabf0700e10fd6a8a79b8a5ccff05683e8c47095049a248ab522e86a; page_uid=8e997147-fa8c-4eb8-9f3d-f7037f89b232',
}

params = (
    ('caller', 'pcweb'),
    ('query', '\uC544\uC6C3\uBC31\uC2A4\uD14C\uC774\uD06C\uD558\uC6B0\uC2A4(\uACF5\uD56D\uC810)'),
    ('type', 'all'),
    ('searchCoord', '126.7947348;37.5633204'),
    ('page', '1'),
    ('displayCount', '20'),
    ('isPlaceRecommendationReplace', 'true'),
    ('lang', 'ko'),
)

response = requests.get('https://map.naver.com/v5/api/search', headers=headers, params=params)

print(response.text)
print(type(response.text))
import json

load = json.loads(response.text)
print(type(load))