from setuptools import setup

setup(
    name="pilogger",
    version="0.1",
    description="Data logging service designed for the Raspberry Pi sense hat and various other sensor peripherals",
    long_description=open("README.md").read(),
    classifiers=[],
    install_requires=["mysql-connector-python"],
    setup_requires=["setuptools_scm", "tox"],
    scripts=[],
    entry_points={},
    zip_safe=False,
    include_package_data=True,
    python_requires=">3.0",
)
