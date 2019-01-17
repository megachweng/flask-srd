"""
flask-consulate
-------------
flask extension that provides an interface to consul via a flask.app
"""

from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'consulate',
    'Flask',
    'requests>=2.7.0',
    'dnspython',
]

setup(
    name='flask-srd',
    version='0.0.1',
    url='http://github.com/megachweng/flask-srd',
    license='MIT',
    author='megachweng',
    author_email='megachweng@gmail.com',

    description='flask extension that provides service registry and discovery functionality',
    long_description=__doc__,

    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=INSTALL_REQUIRES,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
