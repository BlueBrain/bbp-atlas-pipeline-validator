from setuptools import setup, find_packages

setup(
    name="pipeline_validator",
    author="Blue Brain Project, EPFL",
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
    packages=find_packages(),
    url="",
    license="",
    install_requires=[
        "jsonschema>=4.18.4",
        "pytest>=7.4.0",
        "requests>=2.31.0",
        "bigtree[pandas]>=0.10.0",
        "pyJWT>=2.6.0",
    ],
    description="",
    include_package_data=True,
)
