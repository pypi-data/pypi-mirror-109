
from setuptools import setup

setup(
  name='inxaimlflow',
  packages=['inxai-mlflow'],
  version='0.0.2',
  license='MIT',
  description='A library for integration mlflow with inxai library',
  author='Aleksander Profic, Dariusz Tomczyszyn',
  author_email='aleprofic@gmail.com, dariusztomczyszyn@gmail.com',
  url='https://gitlab.com/geist-stud/mlflow-inxai-plugin',
  download_url='https://gitlab.com/geist-stud/mlflow-inxai-plugin.git',
  keywords=['inxai', 'xai', 'mlflow'],
  package_dir={'inxaimlflow': 'inxai-mlflow'},
  install_requires=['mlflow',
                    'lime',
                    'shap',
                    'matplotlib',
                    'seaborn'
                    ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3'
  ],
)