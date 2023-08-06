from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'Readme.md').read_text(encoding='utf-8')

setup(
    name='zts-helloPypi',
    version='0.0.3',
    description='a test for packaging',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='sample,test',
    python_requires='>=3.8, <4',
    install_requires=['readline'],
    url='https://github.com/',
    author='zts2125',
    author_email='786566148@qq.com',
    packages=find_packages(),
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/',
    },
)
