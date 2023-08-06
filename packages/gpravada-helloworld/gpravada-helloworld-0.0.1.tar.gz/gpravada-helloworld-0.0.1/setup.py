from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='gpravada-helloworld',
    version='0.0.1',
    description='Say Hello',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gpravada/gpravada-helloworld",
    author="Gopi Ravada",
    author_email="gp.ravada@gmail.com",
    py_modules=["helloworld"],
    package_dir={'':'src'},
    install_requires = [
        "blessings ~= 1.7",
    ],
    extras_require = {
        "dev":[
            "pytest>=3.7",
        ]
    }
)