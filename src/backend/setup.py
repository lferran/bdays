from setuptools import setup, find_packages


def requirements():
    with open("requirements.txt", "r") as f:
        requirements = f.readlines()
    return requirements


setup(
    name='bdays',
    version='1.0.0',
    url='https://github.com/lferran/bdays.git',
    author='Ferran Llamas',
    author_email='llamas.arroniz@gmail.com',
    description='Birthday reminder app',
    packages=find_packages(),
    install_requires=requirements(),
)
