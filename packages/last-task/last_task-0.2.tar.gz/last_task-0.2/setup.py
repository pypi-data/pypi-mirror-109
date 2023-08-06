from setuptools import setup

setup(name='last_task',
      version='0.2',
      description='last_task',
      url='',
      author='Moontrey',
      author_email='golubev.ruslan2013@yandex.ru',
      packages=['last_task'],
      install_requires=[
            'pandas',
            'scikit-learn',
            'numpy',      
      ],
      include_package_data=True,
      zip_safe=False)
