import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='faostats',
     version='0.113',
     scripts=['faostats'] ,
     author="Daniel Risi",
     author_email="risi.dj@gmail.com",
     description="A package to download faostat data to a postgres database and then analyse it",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/daniel-risi/faostats",
     packages=setuptools.find_packages(),
     install_requires=['pandas', 'sqlalchemy'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent"],
    test_suite = 'nose.collector',
    tests_require = ['nose'],
    include_package_data=True
 )


