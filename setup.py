from setuptools import setup, find_packages

setup(
    name="xml_project_lib",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A library to generate XML project files for video editing software.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/xml_project_lib",
    packages=find_packages(),
    install_requires=[
        "lxml"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
