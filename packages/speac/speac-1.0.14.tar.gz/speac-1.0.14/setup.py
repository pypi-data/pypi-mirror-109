from setuptools import setup, find_packages

# Открытие README.md и присвоение его long_description.
with open("README.md") as f:
    readme = f.read()

setup(
    name='speac',
    version='1.0.14',
    packages=find_packages(),
    url='https://github.com/GolzitskyNikolay/SPEAC-analysis/',
    description='David Cope\'s SPEAC-analysis Python library',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='GlazNik',
    author_email='golzitskij.ns@edu.spbstu.ru',
    keywords='SPEAC David Cope',
    python_requires='>=3.0'
)
