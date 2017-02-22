from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='ckanext-termtranslation',
      version=version,
      description="Add term translations in CKAN from json files.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Valentino Hudhra',
      author_email='v.hudhra@gmail.com',
      url='http://valentinohudhra.com',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [ckan.plugins]
      termtranslation=ckanext.termtranslation.plugin:TermTranslationPlugin

      [paste.paster_command]
	  term_translation = ckanext.termtranslation.commands:TermTranslation

      """,
      )
