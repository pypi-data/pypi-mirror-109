from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3'
]

setup(
    name='kesshashcrackin',
    version='0.0.1',
    description='Hash Cracker',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Ian Moffett',
    author_email='teaqllabs@gmail.com',
    classifiers=classifiers,
    keywords='hash_crack',
    packages=find_packages(),
    install_requires=['']
)