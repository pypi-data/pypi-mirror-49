from setuptools import setup, find_packages

version = "1.1.2"

setup(name="pypgqueue",
      version=version,
      description="A job queue based on PostgreSQL's listen/notify features",
      author="Trey Cucco",
      author_email="fcucco@gmail.com",
      url="https://gitlab.com/tcucco/pypgq",
      download_url="https://gitlab.com/tcucco/pypgq/-/archive/master/pypgq-master.tar",
      packages=["pypgq"],
      package_data={"pypgq": ["ddl.sql"]},
      install_requires=[
        "bidon >= 1.0.4",
        "psycopg2-binary"
      ],
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3 :: Only"
      ],
      license="MIT",
      platforms="any")
