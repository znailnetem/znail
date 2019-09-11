from setuptools import setup, find_packages
from znail import __version__


setup(
    name='znail',

    version=__version__,

    description='Network Emulator',

    maintainer='Andreas Nilsson',
    maintainer_email='andni233@gmail.com',
    url='https://github.com/znailnetem/znail',

    license='Apache License 2.0',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: System :: Networking',
        'Topic :: System :: Emulators',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3.5',
    ],

    keywords='znail',

    packages=find_packages(exclude=['*.test', '*.test.*', 'test.*', 'systest', 'systest.*', 'example', 'example.*']),

    entry_points={
        'console_scripts': [
            'znail = znail.ui.__main__:main',
        ],
    },

    package_data={
        'znail.netem': ['data/*'],
        'znail.ui.web': ['templates/*', 'static/*'],
    },

)
