import pathlib
import setuptools

CURR_DIR = pathlib.Path(__file__).parent.resolve()

VERSION = '0.0.2'
DESCRIPTION = 'Context manager for Sqlite databases'
LONG_DESCRIPTION = (CURR_DIR / "README.MD").read_text(encoding='UTF-8')

# Setting up
setuptools.setup(
    name="sqlite3cm",
    version=VERSION,
    author="Ahmed LAHRIZI",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/ahmedlahrizi/sqlite3_CM",
    keywords=['python', 'sql', "sqlite", "3", "cm", "context", "manage", "database", "db"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
