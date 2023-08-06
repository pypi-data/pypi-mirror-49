from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='clogger',
      version='0.12',
      description='My way python logger configuration',
      long_description=long_description,
      url='https://github.com/pietrogiuffrida/customlogger/',
      author='Pietro Giuffrida',
      author_email='pietro.giuffri@gmail.com',
      license='MIT',
      packages=['clogger'],
      zip_safe=False,
      install_requires=[],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
)
