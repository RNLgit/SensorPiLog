from setuptools import setup

setup(
    name="datalogger",
    version="0.0.1",
    description='RPI sense hat logger and pwm fan controller',
    long_description=open('README.md').read(),
    classifiers=[],
    install_requires=['adafruit-circuitpython-pcf8591'],
    setup_requires=['setuptools_scm', 'tox'],
    scripts=[],
    entry_points={},
    zip_safe=False,
    include_package_data=True,
    python_requires='>3.0'
)
