from setuptools import setup, find_packages

def get_long_description():
    """
    Return the README.
    """
    with open('README.md', encoding="utf8") as fd:
        return fd.read()

setup(
    name='cowin-async',
    version=1.1,
    description='Interact with CoWin APIs',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license="LGPL v3.0",
    author="Prasanna Venkadesh",
    author_email="prasmailme@gmail.com",
    python_requires='>=3.8',
    install_requires=['httpx==0.18.*'],
    extras_require={
        'develop': [
            'pytest==6.2.4',
            'pytest-asyncio==0.15.1',
            'pytest-cov==2.11.1',
            'pytest-httpx==0.12.0'
        ]
    },
    packages=find_packages(exclude=['tests']),
    project_urls={
        "Source": "https://gitlab.com/prashere/cowin-async"
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Framework :: AsyncIO",
        "Framework :: Trio",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only"
    ]
)
