from distutils.core import setup
from os import path
base_dir = path.abspath(path.dirname(__file__))
setup(
  name = 'tulis',        
  packages = ['nulis'],   
  version = '0.0.1',    
  license='MIT',     
  description = 'BOT WRITER', 
  author = 'Krypton Byte',                  
  author_email = 'galaxyvplus6434@gmail.com',     
  url = 'https://github.com/krypton-byte/tulis-module',   
  download_url = 'https://github.com/krypton-byte/tlis-module/archive/0.0.1.tar.gz',    
  keywords = ['nulis', 'tulis', 'writter', 'automate'], 
  install_requires=[           
          'pillow',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)