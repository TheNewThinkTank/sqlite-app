import os, sys, re

# get version info from module without importing it
version_re = re.compile("""__version__[\s]*['|"](.*)['|"]""")

with open('sqlite_app.py') as f:
    content = f.read()
    match = version_re.search(content)
    version = match.group(1)


readme = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(readme).read()


SETUP_ARGS = dict(
    name='sqlite_app',
    version=version,
    description=('Create tables and modify records'),
    long_description=long_description,
    url='https://github.com/TheNewThinkTank/sqlite-app',
    author='Gustav C. Rasmussen'
    author_email='<EMAIL>'
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Database Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
    ],
    py_modules = ['sqlite_app',],
    install_requires = [
        'requests>=2.22',
    ],
)

if __name__ == '__main__':
    from setuptools import setup, find_packages
