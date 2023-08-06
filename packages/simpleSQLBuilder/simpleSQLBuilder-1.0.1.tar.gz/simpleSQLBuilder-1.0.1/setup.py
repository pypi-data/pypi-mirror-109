import setuptools
import simpleSQLBuilder


with open('README.md') as fr:
    long_description = fr.read()


setuptools.setup(
    name='simpleSQLBuilder',
    version=simpleSQLBuilder.__version__,
    author='Silkin S.A.',
    author_email='stas.silkin.2016@gmail.com',
    description='Building queries',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/StAs0n41K/QueryBuilder',
    packages=setuptools.find_packages(),
    install_requires=[],
    test_suite='tests',
    python_requires='>=3.7',
    platforms=["any"]
)