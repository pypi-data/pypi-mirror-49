from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_desc = f.read()

setup(name="django-smart-selects-fix",
      version="1.0",
      description="Django application to handle chained model fields.",
      long_description=long_desc,
      long_description_content_type='text/markdown',
      author="Patrick Lauber",
      author_email="digi@treepy.com",
      url="https://github.com/Murakam1/smart-select-novo",
      packages=find_packages(),
      include_package_data=True,
      tests_require=[
          'flake8',
      ],
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      )
