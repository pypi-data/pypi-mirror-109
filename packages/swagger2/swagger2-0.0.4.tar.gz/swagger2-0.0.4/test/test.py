import json

import swagger2


url = 'https://petstore.swagger.io/v2/swagger.json'
# url = 'http://tdpapi.ygr.iyougu.com/v2/api-docs'
# url = 'http://tmpapi.ygr.iyougu.com/v2/api-docs'

swagger = swagger2.parse(url)

print('转换接口：{}个'.format(len(swagger.apis)))

api_path = 'api.json'
with open(api_path,mode='w',encoding='utf8') as f:
    f.write(json.dumps(swagger.apis,ensure_ascii=False))