from setuptools import setup, find_packages

# Open readme
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lcapy-gui',
    packages=find_packages(include=[
        "lcapygui",
        "lcapygui.*"
    ]),
    version="v0.2.0",
    description="A GUI for lcapy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Michael Hayes, Jordan Hay",
    license="MIT",
    url="https://github.com/mph-/lcapy-gui",
    project_urls={
        "Bug Tracker": "https://github.com/mph-/lcapy-gui",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "lcapy>=1.12",
        "numpy",
        "tk",
        "pillow",
        "matplotlib",
        "svgpathtools",
        "svgpath2mpl"
    ],
    entry_points={
        'console_scripts': [
            'lcapy-tk=lcapygui.scripts.lcapytk:main',
        ],
    },
    include_package_data=True,
    package_data={'': ['data/*.svg']},
    python_requires=">=3.7"  # matched with lcapy
)
