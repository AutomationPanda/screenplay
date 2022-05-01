import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="screenplay",
  version="0.1.0",
  author="Pandy Knight",
  author_email="",
  description="The Python Screenplay Pattern",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/AutomationPanda/screenplay",
  project_urls={
    "Bug Tracker": "https://github.com/AutomationPanda/screenplay/issues",
  },
  classifiers=[
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Testing",
  ],
  package_dir={"": "src"},
  packages=setuptools.find_packages(where="src"),
  python_requires=">=3.7",
)