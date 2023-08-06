import setuptools
import pdf_creator

with open('Readme.md') as fr:
    long_description = fr.read()

setuptools.setup(
    name='pdf_creator',
    version=pdf_creator.__version__,
    author='Lilia Mironova',
    author_email='llmir@inbox.ru',
    description='This library create pdf file',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/liliamir/pdf_creator',
    packages=setuptools.find_packages(),
    install_requires=['reportlab >= 3.5.67',
                      'Pillow >= 8.2.0'],
    test_suite='tests',
    python_requires='>=3.7',
    platforms=["any"]
)