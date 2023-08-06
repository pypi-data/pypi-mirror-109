import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Audiutor-PatBe',
    version='0.0.4',
    license='MIT',
    author="Patrizia Belik",
    author_email='pbelik@unibz.it',
    description='A simple Youtube video transcriber and summarizer',
    long_description = long_description,
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
    package_dir={'': 'src'},
    keywords='Youtube transcriber',  
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
