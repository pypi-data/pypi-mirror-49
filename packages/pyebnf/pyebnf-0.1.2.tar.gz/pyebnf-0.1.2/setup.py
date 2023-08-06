from setuptools import setup, find_packages

version = "0.1.2"

setup(name="pyebnf",
      version=version,
      license="MIT",
      platforms="any",
      author="Trey Cucco",
      author_email="fcucco@gmail.com",
      packages=find_packages(exclude=["tests"]),
      description="An EBNF compiler",
      url="https://github.com/treycucco/pyebnf",
      download_url="https://github.com/treycucco/pyebnf/tarball/master",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4"
      ])
