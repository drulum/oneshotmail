import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oneshotmail",
    version="0.2",
    author="Calum Andrew Morrell",
    author_email="calum@drulum.com",
    description="A simple mailshot package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drulum/oneshotmail",
    project_urls={
        "Bug Tracker": "https://github.com/drulum/oneshotmail/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD 3-Clause License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'pytest',
        'python-dotenv',
    ],
    python_requires=">=3.6",
)
