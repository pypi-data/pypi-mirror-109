import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'pami',
    version = '0.9.6',
    author = 'Rage Uday Kiran',
    author_email = 'uday.rage@gmail.com',
    description = 'Pattern mining',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/udayRage/PAMI.git',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
)
