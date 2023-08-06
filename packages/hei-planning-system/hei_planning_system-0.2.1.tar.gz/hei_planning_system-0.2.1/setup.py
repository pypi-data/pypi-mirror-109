import setuptools
version = {}
with open("planning_system/version.py") as fp:
    exec(fp.read(), version)

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='hei_planning_system',
    version=version['__version__'],
    # py_modules=[],
    author="James Boyes",
    author_email="James.Boyes@lcm.ac.uk",
    description="HE Planning Suite.",
    long_description=long_description,
    url="https://github.com/jehboyes/planning_system",
    packages=setuptools.find_packages(),
    entry_points='''
        [console_scripts]
        plansys=planning_system.cli:ps
    ''',
)
