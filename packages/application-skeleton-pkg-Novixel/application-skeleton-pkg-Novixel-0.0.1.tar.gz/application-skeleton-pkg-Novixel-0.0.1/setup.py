import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="application-skeleton-pkg-Novixel",
    version="0.0.1",
    author="Novixel",
    author_email="Novixel@hotmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Novixel/ApplicationSkeleton",
    project_urls={
        "Bug Tracker": "https://github.com/Novixel/ApplicationSkeleton/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)