import setuptools
import str_srch

with open('Readme.md') as fr:
    long_description = fr.read()

setuptools.setup(
    name='str_srch',
    version='1.0',
    author='Sizykh V.A.',
    author_email='verifikaciya20@mail.ru',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/glynern/str_srch/',
    packages=setuptools.find_packages(),
    install_requires=[],
    test_suite='tests',
    python_requires='>=3.7',
    platforms=["any"]
)