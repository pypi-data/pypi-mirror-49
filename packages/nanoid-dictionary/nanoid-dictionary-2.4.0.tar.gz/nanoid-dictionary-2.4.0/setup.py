from setuptools import setup

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name='nanoid-dictionary',
    version='2.4.0',
    author='Dair Aidarkhanov',
    author_email='dairaidarkhanov@gmail.com',
    description='Predefined character sets to be used with Nano ID',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/aidarkhanov/py-nanoid-dictionary',
    license='MIT',
    packages=['nanoid_dictionary'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ]
)
