from setuptools import setup, find_packages

setup(
    name='kn-yt-downloader',
    version='0.1.0',
    description='Knight YouTube Downloader CLI Tool',
    author='Knight',
    author_email='knight01@gmail.com',
    packages=find_packages(),
    install_requires=[
        'yt-dlp',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'kn-dl=kn_yt_downloader.cli:main'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.8',
)
