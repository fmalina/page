from setuptools import setup, find_packages
import page

setup(
    name="page",
    version=page.__version__,
    description='Replacement for Django contrib flatpages and redirects.',
    long_description=open('README.rst').read(),
    license='BSD License',
    platforms=['OS Independent'],
    keywords='CMS',
    author='F. Malina',
    author_email='fmalina@pm.me',
    url="https://github.com/fmalina/django-page",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split(),
)
