from distutils.core import setup
from Cython.Build import cythonize

setup(name='TwitterAnalyzer',
      version='0.1',
      description='Twitter Analyzer',
      url='https://github.com/scirag/TwitterAnalyzer',
      author='Şafak ÇIRAĞ',
      author_email='safakcirag@gmail.com',
      license='MIT',
      packages=['config', 'crawler', 'daemon', 'model'],
      install_requires=[
          'python>=3.3',
          'Cython',
          'json',
          'redis',
          'pymongo',
          'tweepy',
          'BeautifulSoup4'
      ],
      zip_safe=False,
      ext_modules=cythonize(["daemon/turkish_streaming_pub.py",
                             "daemon/turkish_streaming_sub.py",
                             "crawler/usertimeline.py"])
)
