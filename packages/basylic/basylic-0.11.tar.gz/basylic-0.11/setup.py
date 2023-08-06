from setuptools import setup

setup(
    name='basylic',
    version='0.11',    
    description="Python interface to Basylic's API",
    url='https://github.com/basylic-team/basylic-python-client',
    download_url = 'https://github.com/basylic-team/basylic-python-client/tarball/0.11',
    author='Petar Todorov',
    author_email='ptodorov@etaonis.com',
    license='MIT',
    packages=['basylic'],
    install_requires=['requests>=2.22.0',],
    keywords = ['insurance', 'anti-fraud', 'basylic'], 
    classifiers=[
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
    ],
)