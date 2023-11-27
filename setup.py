from setuptools import setup, find_packages

setup(
    name="pipeline_validator",
    use_scm_version=True,
    packages=find_packages(),
    url="",
    license="",
    install_requires=[
        "jsonschema==4.18.4",
        "pytest==7.4.0",
        "requests==2.31.0",
        "bigtree==0.10.0",
        "pyJWT==2.6.0",
        "logger==1.4",
    ],
    author="platis",
    author_email="",
    description="",
    include_package_data=True,
)
