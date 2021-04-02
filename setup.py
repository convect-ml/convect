import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="convect",
    version="0.0.1-7",
    author="Sameeran Kunche",
    author_email="sameeran@convect.ml",
    description="SDK for Convect",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/convect-ml/convect",
    project_urls={
        "Bug Tracker": "https://github.com/convect-ml/convect/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'dill',
        'requests',
        'notebook',
        'ipykernel',
        'jupyter_contrib_nbextensions',
        'nbconvert<6',
        'pandas>=1.2.0',
        'scikit-learn>=0.24.0',
    ],
    python_requires=">=3.7.1",
)
