from setuptools import setup

setup(
    name="gen",
    version='0.1',
    description="Generate files from a template",
    long_description="Generate files from a template",

    url='http://github.com/pfmoore/gen',

    author='Paul Moore',
    author_email='p.f.moore@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        # Consider adding Python 2 support later...
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],

    keywords='packaging development',
    packages=['gen'],
    install_requires = ['pyyaml'],
    entry_points={
        'console_scripts': [
            'gen=gen:main',
        ],
    },
)
