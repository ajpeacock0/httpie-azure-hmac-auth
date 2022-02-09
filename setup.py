from setuptools import setup

import httpie_azure_hmac

try:
    import multiprocessing
except ImportError:
    pass

setup(
    name='httpie-azure-hmac-auth',
    description='Auth plugin for HTTPie for Azures HMAC format.',
    long_description=open('README.rst').read().strip(),
    version='1.0.0',
    author='Andrew Peacock',
    author=httpie_azure_hmac.__author__,
    license='MIT',
    url='https://github.com/ajpeacock0/httpie-azure-hmac-auth',
    download_url='https://github.com/ajpeacock0/httpie-azure-hmac-auth',
    py_modules=['httpie_azure_hmac'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_azure_hmac = httpie_azure_hmac:AzureHmacPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.7.0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
