from setuptools import setup

setup(name='reescritor',
      version='0.0.4',
      description='A Python module for Spanish Spinner (Reescritor.com & DisparaTusIngresos.com)',
      long_description=open('README.rst').read(),
      long_description_content_type="text/x-rst",
      keywords=['spinner', 'spanish', 'spintax'],
      url='https://github.com/nicolasmarin/reescritor',
      download_url='https://github.com/nicolasmarin/reescritor/archive/refs/heads/main.zip',
      install_requires=[
          'requests',
      ],
      author='nicolasmarin',
      author_email='info@scraping.link',
      license='GPLv3',
      packages=['reescritor'],
      classifiers=[
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          ])
