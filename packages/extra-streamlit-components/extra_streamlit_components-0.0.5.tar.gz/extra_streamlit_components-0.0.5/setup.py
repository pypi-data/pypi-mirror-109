import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="extra_streamlit_components",
    version="0.0.5",
    author="Mohamed Abdou",
    author_email="matex512@gmail.com",
    description="An all-in-one place, to find complex or just not available components by default on streamlit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mohamed-512/Extra-Streamlit-Components",
    packages=['extra_streamlit_components'],
    include_package_data=True,
    classifiers=[],
    keywords=['Python', 'Streamlit', 'React'],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
