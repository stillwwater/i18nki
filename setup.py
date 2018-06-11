from setuptools import setup, find_packages

setup(name='i18nki',
      version='0.1',
      author='Lucas',
      author_email='stillwwater@gmail.com',
      license='MIT',
      description='Internationalization/Localization Key Interpreter',
      url='https://github.com/stillwwater/i18nki',
      install_requires=['colorama', 'argparse'],
      packages=find_packages(exclude=('.git')))
