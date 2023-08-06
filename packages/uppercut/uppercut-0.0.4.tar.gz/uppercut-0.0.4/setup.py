from setuptools import setup,find_packages
print('A')
setup(
    name='uppercut',
    url='https://github.com/StephanAm/uppercut.python.tools',
    author='Stephan Marais',
    maintainer='Stephan Marais',
    version='0.0.4',
    description='A library to handle common tasks for creating an Uppercut module in python.',
    py_modules=['test'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7"
    ],
)