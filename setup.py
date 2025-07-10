from setuptools import setup, find_packages

setup(
    name="remoteok-scraper",
    version="0.1.0",
    description="A simple RemoteOK job scraper.",
    packages=find_packages(),
    include_package_data=True,  # so that config.yml is packaged
    install_requires=[
        "requests>=2.20.0",
        "pandas>=1.0.0",
        "pyyaml>=5.4",
        "pyarrow>=2.0.0",
        "matplotlib>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "scrape-jobs=remoteok_scraper.scraper:main",
        ],
    },
)
