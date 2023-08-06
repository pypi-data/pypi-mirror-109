import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Audiutor-PatBe", # Replace with your own username
    version="0.0.2",
    author="Patrizia Belik",
    author_email="pbelik@unibz.it",
    description="Youtube English video transcriber and summarizer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
      'pytube',
      'ibm_watson',
      'ffmpeg-python',
      'nltk',
      'wordcloud',
      'matplotlib',
      'textacy==0.9.1',
      'spacy==2.3.5',
      'python-docx', 
    ],    
)