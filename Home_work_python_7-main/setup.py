from setuptools import setup, find_namespace_packages


setup(name='clean-folder',
      version='0.3',
      description='Do sort files',
      url='https://github.com/last-war/Home_work_python_6',
      author='Last_war',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': [
          'clean-folder = clean_folder.my_sort:main']}
      )
