from setuptools import setup

setup(name='pynasdaq',
      version='0.1.0',
      description='Retrieve NASDAQ stock and dividend data',
      url='https://github.com/makkader/pynasdaq',
      author='Mak Kader',
      author_email='abdul.kader880@gmail.com',
      license='MIT',
      packages=['pynasdaq'],
      install_requires=[
          'pandas',
          'lxml',
          'requests'
      ],
      zip_safe=False)
