from setuptools import setup

setup(
    name='cryptochecker',
    version='0.0.5',
    description='Check any Bitcoin and Ethereum transaction',
    long_description_content_type='text/markdown',
    url='https://github.com/Aegar6/cryptochecker',
    author='Aegar6',
    author_email='bogusz.krzyzanow@gmail.com',
    keywords='crypto cryptocurrency cryptochecker bitcoin ethereum',
    license='MIT',
    python_requires='>=3.6',
    packages=['cryptochecker'],
    classifiers=['Programming Language :: Python :: 3'],
    install_requires=['requests','selectorlib']
)
