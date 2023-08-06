import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tl2",
    version="0.0.2",
    author="Peterou",
    author_email="pengzhoucv@gmail.com",
    description="A personal package for research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PeterouZh/tl2",
    packages=setuptools.find_packages(),
    install_requires=[
        # 'Django >= 1.11, != 1.11.1, <= 2',
        'easydict'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)




