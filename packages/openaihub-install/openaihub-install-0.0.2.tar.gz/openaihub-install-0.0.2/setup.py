import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openaihub-install",
    version="0.0.2",
    author="Adrian Zhuang",
    author_email="wzhuang@us.ibm.com",
    description="OpenAIHub installer and others",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.ibm.com/OpenAIHub/OpenAIHub",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'click',
        'GitPython',
        'wget'
    ],
    entry_points='''
        [console_scripts]
        openaihub=openaihub.cli:cli
    '''
)
