from setuptools import setup
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='avrs-web',
    version='0.1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    exclude_package_date={'': ['.gitignore']},
    zip_safe=False,
    author="Yen C. Li",
    description="An associated videos recommendation system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yencli/avrs-web",
    keywords="nlp clustering embeddings unsupervised topics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License version 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'bokeh',
        'Flask',
        'hdbscan',
        'numpy',
        'pandas',
        'sentence_transformers',
        'spacy',
        'umap_learn'
    ]
)
