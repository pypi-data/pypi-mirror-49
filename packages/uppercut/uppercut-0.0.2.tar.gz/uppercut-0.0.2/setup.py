from setuptools import setup
print('A')
setup(
    name='uppercut',
    url='https://github.com/StephanAm/uppercut.python.tools',
    author='Stephan Marais',
    maintainer='Stephan Marais',
    version='0.0.2',
    description='A library to handle common tasks for creating an Uppercut module in python',
    py_modules=['test'],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3.7"
    ],
)