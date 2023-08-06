from setuptools import setup

'''
安装Twine： 
    # pip install twine

打包发布：
    1.修改setup.py文件版本号
    2.删除历史发布目录dist、build
    3.使用setuptools打包: 
        # python setup.py sdist
        # python setup.py install 
    4.使用twine发布到pypi:
        # python -m twine upload dist/* 
    
参考文档：
    https://setuptools.readthedocs.io/en/latest/references/keywords.html
    https://packaging.python.org/tutorials/packaging-projects/#setup-args

备注：
    需要setuptools工具配合twine工具才能使用markdown文档

实用脚本：
    import subprocess
    import shutil
    import os

    dir_list = ['build','dist','ljh_example.egg-info']
    for dir in dir_list:
        if os.path.exists(dir):
            shutil.rmtree(dir)

    res = subprocess.check_output('python setup.py sdist')
    print(res.decode())
    res = subprocess.check_output('python setup.py install')
    print(res.decode())
    res = subprocess.check_output('python -m twine upload dist/*',shell=True)
    print(res.decode('gbk'))
'''

desc_doc = 'README.md'

setup(
    name='swagger2',
    version='0.0.4',
    author='Jinghe Li',
    author_email='2981160914@qq.com',
    url='https://gitee.com/ppbug',
    # download_url='http://www.baidu.com',
    py_modules=[],
    packages=['swagger2'],
    # scripts=['ljh_example.py'],
    entry_points={
        # 'console_scripts': ['adb_init = ljh_example:init']
    },
    install_requires=[
        'requests'
    ],
    description='实现了Swagger文档生成Python请求数据功能，借助主流测试框架可快速完成大批量的接口测试任务',
    long_description_content_type='text/markdown',
    long_description=open(desc_doc, encoding='utf-8').read(),
)
