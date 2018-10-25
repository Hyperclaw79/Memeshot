import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='memeshot',
    version='0.1',
    packages=['memeshot', 'tests']
    scripts=['subgrab.py', 'shotgrab.py'],
    author="Harshith Thota",
    author_email="harshith.thota7@gmail.com",
    description="""
        Grab screenshots from videos based on a search word in subtitles.
        You can use it get images from videos to create dope memes.
    """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hyperclaw79/memeshot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        'Natural Language :: English'
        'Topic :: Meme Screenshots'
    ],
 )
