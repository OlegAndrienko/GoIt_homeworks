from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='0.1',
      description='Sort files code',
      url='https://github.com/OlegAndrienko/GoIt_homeworks/blob/master/',
      author='Andrienko O.',
      author_email='olegandrienko@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean = clean_folder.clean:main']}
      )
