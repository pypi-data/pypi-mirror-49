from setuptools import setup, find_packages
 




setup(name='cubestories',
      version='0.3.5',
      url='https://github.com/MaciejJanowski/CubeStories',
      license='MIT',
      author='Maciej Janowski',
      author_email='maciej.janowski@insight-centre.org',
      description='CuebStories',
      packages=find_packages(exclude=["tests"]),
      #package_dir={"CubeStories":"CubeStories"},
      install_requires=['SPARQLWrapper>=1.8.4,<1.8.5',
                        'sparql_dataframe>=0.1,<0.2',
                        'pandas>=0.24.2,<0.25.0',
                        'datastories',
                        'numpy>=1.16.2,<1.16.3',
                        'scipy>=1.2.1,<1.2.2'],
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False)
