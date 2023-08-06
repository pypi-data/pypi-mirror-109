from setuptools import setup
from pathlib import Path


setup(name='cue',
      version='0.9',
      description='Accounting system for linux',
      long_description=Path('README.md').read_text(),
      long_description_content_type='text/markdown',
      author='Jonas McCallum',
      author_email='jonasmccallum@gmail.com',
      url='https://kosciuszko.cloud',
      packages=['cue',
                'cue.cli'],
      package_data={
          '': ['templates/*.yml',
               'templates/*.txt']
      },
      license_files=('LICENSE.txt'),
      install_requires=['ruamel.yaml',
                        'wheezy.template'],
      extras_require={'testing': ['pytest']},
      entry_points={'console_scripts': ['cue = cue.cli.bin:cue']},
      project_urls={
          'Source': 'https://bitbucket.org/kosciuszko/cue',
          'Tracker': 'https://bitbucket.org/kosciuszko/cue/issues',
      },
      zip_safe=False)
