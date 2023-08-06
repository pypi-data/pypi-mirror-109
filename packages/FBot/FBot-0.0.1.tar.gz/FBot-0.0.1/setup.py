from setuptools import setup, find_packages

classiefiers = [
    'Developement Status :: 5 - Production/Stable',
    'Intended Auidence :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10 :: Linux',
    'Licence :: OSI Approved :: MIT Lience',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'FBot',
    version = '0.0.1',
    description = 'FBot - A python liabrary, In which you can generate chat bots effortlessly.',
    Long_description = open('README.md').read(),
    url = 'https://github.com/back-2-hack',
    author = 'B2H',
    author_email = 'back2hacck@gmail.com',
    License = 'MIT',
    classiefiers = classiefiers,
    keywords = 'chat_bot',
    packages = find_packages(),
    install_requires = ['fuzzywuzzy']
)
