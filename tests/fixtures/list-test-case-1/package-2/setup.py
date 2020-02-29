from setuptools import setup

setup(
    name="package-2",
    install_requires=["MarkupSafe==8.3.2", "psycopg2==2.3",],
    extras_require={"test": ["autoflake==3.2",],},
)
