# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tencentcos_storage']

package_data = \
{'': ['*']}

install_requires = \
['cos-python-sdk-v5>=1.9.4,<2.0.0']

setup_kwargs = {
    'name': 'django-tencentcos-storage',
    'version': '0.1.0',
    'description': 'A django app for Tencent Cloud Object Storage. 腾讯云对象存储（COS）服务 for Django。',
    'long_description': '# Django TencentCOS Storage\n\n腾讯云对象存储（COS）服务 for Django。\n\n## 环境要求\n\nPython: >=3.7, <4\n\nDjango: >=2.2, <3.3\n\n## 安装\n\n```\npip install django-tencentcos-storage\n```\n\n## 基本使用\n\n在项目的 settings.py 中设置 `DEFAULT_FILE_STORAGE`：\n\n```python\nDEFAULT_FILE_STORAGE = "tencentcos_storage.TencentCOSStorage"\n```\n\n此外，还需要设置腾讯云对象存储服务相关的必要信息：\n\n```python\nTENCENTCOS_STORAGE = {\n    "BUCKET": "存储桶名称",\n    "CONFIG": {\n        "Region": "地域信息",\n        "SecretId": "密钥 SecretId",\n        "SecretKey": "密钥 SecretKey",\n    }\n}\n```\n\n详情可参考 [腾讯云对象存储官方文档](https://cloud.tencent.com/document/product/436)\n\n## 设置\n\n### 示例\n```python\nTENCENTCOS_STORAGE = {\n    # 存储桶名称，必填\n    "BUCKET": "存储桶名称",\n    # 存储桶文件根路径，默认 \'/\'\n    "ROOT_PATH": "/",\n    # 腾讯云存储 Python SDK 的配置参数，详细说明请参考腾讯云官方文档\n    "CONFIG": {\n        "Region": "地域信息",\n        "SecretId": "密钥 SecretId",\n        "SecretKey": "密钥 SecretKey",\n    }\n}\n```\n\n### 说明\n\n**BUCKET**\n> 存储桶名称，必填\n\n**ROOT_PATH**\n> 文件根路径，默认为 \'/\'\n\n**CONFIG**\n> 腾讯云对象存储 Python SDK 的配置参数，其中 `Region`、`SecretId`、`SecretKey` 为必填参数。\n> \n> 关于配置参数的详细说明请参考 [腾讯云对象存储 Python SDK 官方文档](https://cloud.tencent.com/document/product/436/12269)\n\n',
    'author': 'jukanntenn',
    'author_email': 'jukanntenn@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jukanntenn/django-tencentcos-storage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
