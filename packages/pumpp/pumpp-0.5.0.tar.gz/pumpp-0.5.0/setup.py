from setuptools import setup, find_packages

import imp

version = imp.load_source('pumpp.version', 'pumpp/version.py')

setup(
    name='pumpp',
    version=version.version,
    description="A practically universal music pre-processor",
    author='Brian McFee',
    url='http://github.com/bmcfee/pumpp',
    download_url='http://github.com/bmcfee/pumpp/releases',
    packages=find_packages(),
    long_description="A practically universal music pre-processor",
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords='audio music learning',
    license='ISC',
    install_requires=['librosa>=0.6.2',
                      'jams>=0.3',
                      'scikit-learn>=0.20',
                      'mir_eval>=0.5'],
    extras_require={
        'docs': ['numpydoc'],
        'tests': ['pytest', 'pytest-cov', 'keras', 'tensorflow'],
        'keras': ['keras'],
    }
)
