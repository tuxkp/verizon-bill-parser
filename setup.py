from setuptools import setup, find_packages

setup(
    name='verizon_bill_parser',
    version='0.1',
    packages=['verizon_bill_parser'],
    install_requires=[
        'pdfminer.six'
    ],
    url='https://github.com/amitrke/verizon-bill-parser',
    author='Amit Kumar',
    author_email='',
    description='A simple parser for Verizon bill PDFs',
)