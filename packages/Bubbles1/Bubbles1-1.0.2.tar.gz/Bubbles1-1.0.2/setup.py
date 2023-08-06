from setuptools import find_packages, setupsetup(    name='Bubbles1',    packages=find_packages(include=['Bubbles1']),    version='1.0.2',    description='Kinetiq_Library',    long_description=open('read.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],    author='Sujata',
    include_package_data=True,    license='MIT',    install_requires=[''],
    entry_points={
        "console_scripts": [
            "Demo_video=Bubbles1.Demo_video:main",
        ]
    },)