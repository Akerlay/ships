from setuptools import setup, find_packages

setup(
    name='ships',
    version='1.0',
    author='akerlay',
    packages=find_packages(),
    python_requires='>=3.7',
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.7',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'app = app.app:main',
        ]
    },
)
