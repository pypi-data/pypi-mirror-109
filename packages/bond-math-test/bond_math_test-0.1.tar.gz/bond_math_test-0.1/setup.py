from setuptools import setup, find_packages

setup(name='bond_math_test',
      version='0.1',
      description='test math package',
      long_description='university project math package.',
      classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
      keywords='python Math',
      url='http://github.com',
      author='J_Bond',
      author_email='J_Bond@example.com',
      packages=find_packages(),
      install_requires=[
          'nympy'
      ],
      include_package_data=True,
      zip_safe=False)