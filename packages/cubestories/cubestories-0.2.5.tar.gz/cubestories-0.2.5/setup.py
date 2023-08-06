from setuptools import setup, find_packages
 




setup(name='cubestories',
      version='0.2.5',
      url='https://github.com/MaciejJanowski/CubeStories',
      license='MIT',
      author='Maciej Janowski',
      author_email='maciej.janowski@insight-centre.org',
      description='CuebStories',
      packages=find_packages(),
      #package_dir={"CubeStories":"CubeStories"},
      install_requires=['SPARQLWrapper',
                        'sparql_dataframe','pandas',
                        'datastories',
                        'numpy','scipy'],
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False)
