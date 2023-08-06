from distutils.core import setup
setup(
  name = 'pyvec',         
  py_modules=["iters", "vector"],  
  version = '0.2',     
  license='MIT',       
  description = 'Poor c++ vector implementation for python',   
  author = 'cvsae',                  
  author_email = 'cvsc@gmx.com',     
  url = 'https://github.com/cvsae/pyvec',   
  download_url = 'https://github.com/cvsae/pyvec/archive/v_02.tar.gz',
  keywords = ['vector', 'python', 'c++', "implementation"],   
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Topic :: Software Development :: Build Tools',    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 2.7',
  ],
)
