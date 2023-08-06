from setuptools import setup, find_packages

def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()

version = dict()
with open("./dominions/utils/version.py") as fp:
    exec(fp.read(), version)


setup(
    name='dominions',
    version=version['__version__'],
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A Python package to check a domain against confusables, levenshtein distance, and more using a single interface. A Python package created using carcass',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=parse_requirements('./requirements.txt'),
    keywords=['carcass'],
    url='https://github.com/swimlane/dominions',
    author='MSAdministrator',
    author_email='rickardja@live.com',
    python_requires='>=3.6, <4',
    package_data={
        'dominions':  ['data/logging.yml']
    },
    entry_points={
          'console_scripts': [
              'dominions = dominions.__main__:main'
          ]
    }
)