import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='BaseGong',
    version='2.1',
    author='gong',
    author_email='2976560783@qq.com',
    description='A small example',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/2976560783/GongUtil',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)