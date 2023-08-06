from setuptools import setup, find_packages

setup(name='miditeach',
    version='0.3',
    description='miditeach',
    url='https://github.com/alelouis/midiTeach',
    author='Alexis LOUIS',
    author_email='alelouis.dev@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['miditeach=miditeach.miditeach:main'],
    },
    install_requires=[
        'arcade',
        'python-rtmidi',
        'mido'
    ],
    zip_safe=False)