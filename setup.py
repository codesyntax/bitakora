from setuptools import setup, find_packages
import os

version = "1.0"

setup(
    name="bitakora",
    version=version,
    description="Django project. ",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=["Framework :: Django", "Programming Language :: Python"],
    keywords="django",
    author="",
    author_email="",
    url="http://code.codesyntax.com/private/",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "mysqlclient",
        "django-photologue==3.9",
        "django-sortedm2m",
        "django-recaptcha",
        "django-voting",
        "django-tinymce",
        "django-haystack",
        "django-bootstrap-form",
        "django-pagination-bootstrap",
        "django-contact-form",
        "django-registration-redux",
        "pytz",
        # -*- Extra requirements: -*-
        "django-storages",
        "raven",
        "bleach",
        "akismet",
        "gunicorn",
        "django-user-agents",
    ],
    entry_points="""
      # -*- Entry points: -*-
      """,
)
