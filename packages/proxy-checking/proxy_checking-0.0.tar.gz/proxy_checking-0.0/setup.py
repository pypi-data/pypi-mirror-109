import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='proxy_checking',
    version='0.0',
    packages=['proxy_checking'],
    install_requires=['certifi==2021.5.30', 'chardet==4.0.0', 'idna==2.10', 'PySocks==1.7.1', 'requests==2.25.1', 'urllib3==1.26.5'],
    author='Pro100git',
    description='A checker designed in Python 3 for checking proxy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='proxy checker python3',
    project_urls={
        'Source Code': 'https://github.com/pro100git/proxy_checker'
    },
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ]
)
