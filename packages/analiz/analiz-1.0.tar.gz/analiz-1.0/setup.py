from setuptools import setup

README_PATH = "README.md"
f = open(README_PATH, "r", encoding="utf-8")
longDesc = f.read()
f.close()

setup(
    name='analiz',
    version='1.0',
    packages=['analiz','analiz.zaman_serileri', 'analiz.dogrusal_regresyon', 'analiz.karar_agaci'],
    url='http://asadasd.com',
    download_url='https://www.ilkeryolundagerek.com',
    license='afl-3.0',
    author='ilker yolunda gerek',
    author_email='a@a.net',
    description=longDesc,
    keywords=["Key1", "Key2", "Key3"],
    install_requires=['pandas', 'requests', 'numpy']
)
