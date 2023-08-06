"""
"""
from codecs import open
from os import path

from setuptools import setup, find_packages

current_dir = path.abspath(path.dirname(__file__))
long_description = __doc__

with open(path.join(current_dir, "CHANGELOG.md"), encoding="utf-8") as f:
    long_description += "\n" + f.read()

classifiers = ["License :: OSI Approved :: MIT License",
               "Topic :: Software Development",
               "Topic :: Utilities",
               "Operating System :: Microsoft :: Windows",
               "Operating System :: MacOS :: MacOS X"] + [
                  ("Programming Language :: Python :: %s" % x) for x in "3.4 3.5 3.6 3.7 3.8".split()]


def command_line():
    target = "xmind2json.main:main"
    entry_points = []
    entry_points.append("xmind2json=%s" % target)
    return entry_points


def main():
    setup(
        name="xmind2json",
        description="Convert xmind to json or xml file.",
        keywords="xmind parser converter json xml",
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=classifiers,
        version="1.1.0",
        author="hichencanxin",
        author_email="hichencanxin@qq.com",
        url="https://github.com/chencanxin/xmind2json",
        packages=find_packages(exclude=['tests', 'tests.*']),
        package_data={},
        install_requires=[],
        entry_points={"console_scripts": command_line(), },
        zip_safe=False
    )


if __name__ == "__main__":
    main()
