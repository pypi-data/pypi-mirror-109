import unittest
import requests
import os
import warnings

import swagger2

from swagger2 import utils


class APITestCase(unittest.TestCase):
    default_file = 'file.txt'

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore',ResourceWarning)
        # 准备测试资源
        if not os.path.exists(cls.default_file):
            with open(cls.default_file, mode='w') as f:
                f.write('Hello world!')

        url = 'https://petstore.swagger.io/v2/swagger.json'

        cls.swagger = swagger2.parse(url,verify=False)

    @classmethod
    def tearDownClass(cls):
        # 清理测试资源
        if os.path.exists(cls.default_file):
            os.remove(cls.default_file)

    def test_apis(self):
        for api in self.swagger.apis:
            with self.subTest(api.get('name')) as st:
                # 请求地址
                url = api.get('url')
                # 请求方法
                method = api.get('method')
                # 请求头
                headers = api.get('headers')
                # 路径参数
                paths = api.get('paths')
                # 查询字串，即query string
                params = api.get('query')
                # 普通表单，即 Content-Type = application/x-www-form-urlencoded
                data = api.get('form')
                # 文件表单, 即 Content-Type = multipart/form-data
                formData = api.get('formData')

                # json格式的参数, 即 Content-Type = application/json
                payload = api.get('json')

                # 文件上传时建议用requests框架的请求头
                if headers.get('Content-Type') == 'multipart/form-data':
                    del headers['Content-Type']
                # 路径参数格式化
                url = utils.path_format(url, paths)

                # 文件表单参数格式化
                formData = utils.form_format(formData)

                res = requests.request(method=method,
                                       url=url,
                                       headers=headers,
                                       params=params,
                                       data=data,
                                       files=formData,
                                       json=payload,
                                       timeout=30,
                                       verify=False)
                print(res.text)
                self.assertTrue(res.ok)


if __name__ == '__main__':
    unittest.main()