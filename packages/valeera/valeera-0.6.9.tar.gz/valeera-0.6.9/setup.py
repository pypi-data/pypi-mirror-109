from setuptools import find_packages, setup

setup(
  name='valeera',
  description='Validator for district42 schema',
  version='0.6.9',
  url='https://github.com/nikitanovosibirsk/valeera',
  author='Nikita Tsvetkov',
  author_email='nikitanovosibirsk@yandex.com',
  python_requires='>=3.6',
  license='MIT',
  packages=find_packages(),
  install_requires=[
    'district42<1.0',
  ],
)
