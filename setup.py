from setuptools import setup, find_packages
import fpage

setup(
    name="f-page",
    version=fpage.__version__,
    description='Static site generator.',
    long_description=open('README.rst').read(),
    license='BSD License',
    platforms=['OS Independent'],
    keywords='CMS',
    author='F. Malina',
    author_email='fmalina@pm.me',
    url="https://github.com/fmalina/f-page",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split(),
)
