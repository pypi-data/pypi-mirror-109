from setuptools import setup, find_packages

setup(
    name = "ylx-tools",
    version = "0.0.1",
    description = "",
    long_description = "",

    author = "ylx",
    author_email = "LLK284154336@outlook.com",

    packages = find_packages(),
    include_package_data = True,
    classifiers = [
        'Programming Language :: Python :: 3',
      ],
    install_requires = [
        'pymysql>=1.0.2',
        'influxdb>=5.3.1'
        'requests>=2.25.1'
]
)