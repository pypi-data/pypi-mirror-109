from setuptools import find_packages, setup


NAME='lesscode'
VERSION='0.0.1'

packages = find_packages(exclude=["instance","tests.*", "tests", "requirements", "deploy","docs"])

setup(
    name=NAME,
    version=VERSION,
    entry_points={'console_scripts': [
        f'{NAME}={NAME}:cli',
        # [[[cog 
        # if values.extensions['desktop.py'].enabled:
        #   p("f'{NAME}-ui={NAME}:ui',\n")
        # ]]]
        # [[[end]]]        
        ]},
    python_requires=">3.7.0",
    packages=packages,
    extras_require={},
    include_package_data=True,
    install_requires=[],
    test_suite="tests",
)
