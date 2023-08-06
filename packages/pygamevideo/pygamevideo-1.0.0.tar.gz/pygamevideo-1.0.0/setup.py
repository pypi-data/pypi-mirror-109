from setuptools import setup, find_packages
import os

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, path)

setup(
    name="pygamevideo",
    packages = find_packages(),
    #data_files=[('libs', ['keys.py', "terminal.py"]), ('', ['favicon.png'])],
    include_package_data=True,
    version="1.0.0",
    author="Kadir Aksoy",
    author_email="kursatkadir014@gmail.com",
    description="Video player for Pygame",
    url="https://github.com/kadir014/pygamevideo",
    project_urls={
    'Documentation': 'https://github.com/kadir014/pygamevideo/README.md#Reference',
    },
    keywords='python pygame video mp4 media',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=open("requirements.txt", "r").readlines()
)
