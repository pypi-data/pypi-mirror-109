from setuptools import setup
import pypandoc

long_description = pypandoc.convert('README.md', 'rst')

setup(
    name='bbdraw',
    version='0.1',
    packages=['bbdraw'],
    url='https://github.com/krasch/bbdraw',
    license='MIT',
    author='krasch',
    author_email='dev@krasch.io',
    description='Library for drawing labeled bounding boxes / bounding polygons',
    long_description=long_description,
    python_requires=">=3.5",
    install_requires=['pillow>=4.0'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'],
)