import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

github_url = "https://github.com/j3soon/org2ical"

setuptools.setup(
    name="org2ical",
    version="0.0.2",
    author="Johnson",
    author_email="j3.soon777@gmail.com",
    description="Generate a iCalendar (.ics) file based on a OrgMode (.org) file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=github_url,
    project_urls={
        "Issues": f"{github_url}/issues",
        "Source Code": github_url,
    },
    keywords=(
        "package, parser, converter, python, orgmode, icalendar"
    ),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where=".", exclude=("tests*",)),
    install_requires=[
        # TODO: Add orgparse after merged
    ],
    extras_require={
        "testing": ["pytest", "mypy", "flake8", "pylint", "icalendar", "python-dateutil"],
    },
)

# Note: PyPI seems to only recognize double-quoted strings
