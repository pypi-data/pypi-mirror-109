import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="humsithon",
    version="0.0.1",
    author="ALHUMSI",
    author_email="jjsjs@gmail.com",
    description="سورس حماية مجموعات تليجرام",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alhomsidev/humsithon",
    project_urls={
        "Bug Tracker": "https://t.me/api_tele",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
