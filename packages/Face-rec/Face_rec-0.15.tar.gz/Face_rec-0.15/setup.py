#from distutils.core import setup
from setuptools import setup,find_packages
setup(
  name = 'Face_rec',         # How you named your package folder (MyLib)
  packages =find_packages(), 
  #packages = ['Face_rec'],   # Chose the same as "name"
  include_package_data=True,
  version = '0.15',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python face recognition library',   # Give a short description about your library
  author = 'SOUHARDYA ADHIKARY',                   # Type in your name
  author_email = 'souhardyaadhikary86942@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/SOUHARDYAADHIKARY1999/Face_rec_pip',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/SOUHARDYAADHIKARY1999/Face_rec_pip/archive/refs/tags/v_0.15.tar.gz',    
  keywords = ['FACE', 'RECOGNITION', 'PERSONALITIES'],   # Keywords that define your package best
  install_requires=[            
          'keras',
          'opencv-python',
          'numpy',
          'tensorflow',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',    #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
  ],
)