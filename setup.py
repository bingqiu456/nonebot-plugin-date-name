
 # -*- coding: utf-8 -*-
import setuptools
setuptools.setup(
    name = "nonebot_plugin_date_name",
    version = "1.0",
    packages = setuptools.find_packages(),
    author="bingyue",
    author_email="hello-yiqiu@qq.com",
    description="""让你的群昵称显示现在时间""",
    url="https://github.com/bingqiu456/nonebot_plugin_date_name",
    install_requires=[
        "nonebot2>=2.0.0b2",
        "Pillow>=9.1.1",
        "nonebot-adapter-onebot>=2.0.0b1",
        "nonebot-plugin-apscheduler>=0.1.3"
    ],
    keywords=["nonebot_plugin_date_name","nonebot","nonebot_plugin"],
)