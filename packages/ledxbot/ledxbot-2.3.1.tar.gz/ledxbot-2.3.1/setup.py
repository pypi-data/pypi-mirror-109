from setuptools import setup, find_packages
import codecs
import os

VERSION = '2.3.1'
DESCRIPTION = 'a advanced bot for fortnite'
LONG_DESCRIPTION = 'You want your Short Description to be 2 to 3 sentences and the rest of your content in the Long Description. Not only does the Short Description help you with SEO but it also used for marketplaces such as Google Products, TheFind, Amazon, etc.  Please do not stick HTML code in the Short Description as it might cause the product not to be sent to these marketplaces.'

# Setting up
setup(
    name="ledxbot",
    version=VERSION,
    author="Led (HarryD)",
    author_email="<ledxbotofficial@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['aiofiles', 'aiohttp', 'fortnitepy', 'sanic', 'BenBotAsync', 'FortniteAPIAsync', 'crayons'],
    keywords=['python', 'sanic', 'BenBotAsync', 'FortniteAPIAsync'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
