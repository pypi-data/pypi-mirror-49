from setuptools import setup

with open('README.md', "r") as readme_file:
    long_description = readme_file.read()

setup(
    name='imgload',
    version='0.2.0',
    description='An image downloading library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["imgload"],
    install_requires=['requests-html', 'pillow'],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/frenos/imgload",
    author="frenos",
)
