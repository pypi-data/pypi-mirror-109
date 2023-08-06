import setuptools

with open ( "README.md" ) as file:
    README_description = file.read (  )

setuptools.setup (
    name = "MyFileInfoLib",
    version = "0.2",
    author = "Alina Filippova",
    author_email = "alia.filippova.2002k@mail.ru",
    description = "This library gets some information about a couple of files.",
    long_description = README_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/alina-filippova/MyFileInfoLib.git",
    packages = [ 'MyFileInfoLib' ],
    classifilers = [
        "Programming language :: Python :: 3",
        "License :: MIT Liesense",
        "Operating System :: Windows"
    ],
    python_requires = '>=3.9'
)