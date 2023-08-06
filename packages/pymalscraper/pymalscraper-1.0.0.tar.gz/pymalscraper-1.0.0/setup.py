from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pymalscraper',
      version='1.0.0',
      author='prinsepipo',
      author_email='prinse.sanchez@gmail.com',
      description='Simple Anime Web Scraper.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/prinsepipo/pymalscraper',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
      install_requires=[
          'requests',
          'beautifulsoup4',
          'lxml'
      ],
      zip_safe=False)
