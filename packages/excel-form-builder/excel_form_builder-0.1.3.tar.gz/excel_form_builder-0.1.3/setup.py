from setuptools import setup

setup(name='excel_form_builder',
      version='0.1.3',
      description='Convert XLSX to JSON',
      author='Anthony Seliga',
      author_email='anthony.seliga@gmail.com',
      license='MIT',
      packages=['excel_form_builder'],
      install_requires=[
          'openpyxl',
          'colorama',
      ],
      scripts=['bin/create_form.py'],
      zip_safe=False)
