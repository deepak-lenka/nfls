from setuptools import setup, find_packages

setup(
    name="nfl-analysis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'crewai>=0.1.0',
        'beautifulsoup4',
        'requests',
        'pandas',
        'numpy',
        'selenium',
        'webdriver_manager',
        'python-dotenv',
        'openai',
        'langchain'
    ],
) 