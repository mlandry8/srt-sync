""" Setup File for srtsync
"""

import setuptools

setuptools.setup(
    name="srtsync",
    version="0.0.5",
    author="Michael Landry",
    author_email="mlandry8@outlook.com",
    description="batch srt time syncing",
    url="https://github.com/mlandry8/srtsync",
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]
)
