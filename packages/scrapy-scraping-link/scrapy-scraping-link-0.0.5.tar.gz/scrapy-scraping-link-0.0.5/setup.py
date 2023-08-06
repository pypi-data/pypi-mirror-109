from setuptools import setup

setup(
    name='scrapy-scraping-link',
    version='0.0.5',
    url='https://github.com/nicolasmarin/scrapy-scraping-link',
    description='Scrapy middleware for Scraping.link',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['web scraping', 'scraping', 'proxy rotating', 'html'],
    download_url='https://github.com/nicolasmarin/scrapy-scraping-link/archive/refs/heads/main.zip',
    install_requires=[
        'scrapy',
    ],
    author='Nicolas Marin',
    author_email='info@scraping.link',
    license='MIT',
    packages=['scrapy_scraping_link'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Scrapy',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.5',
)
