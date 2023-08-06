from distutils.core import setup
setup(
  name = 'standard_scaler',
  packages = ['standard_scaler'],
  version = '0.3',     
  license='MIT',    
  description = 'An alternative to scikit-learn standard scaler', 
  author = 'Hart Massie-Keller',
  author_email = 'hartktraveller@gmail.com', 
  url = 'https://github.com/hartktmk/standard_scaler',
  download_url = 'https://github.com/hartktmk/standard_scaler/archive/refs/tags/0.3.tar.gz',
  keywords = ['standard', 'scaler', 'scaling','transform','ml','ai'],
  install_requires=[ 
          'numpy'
      ]
)