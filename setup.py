from setuptools import setup, find_packages


setup(
    name='inno_moodle_crawld',
    version='0.0.1',
    description='Innopolis Moodle parser',
    author='Leonid Lygin',
    author_email='ionagamed@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'crawld'
    ],
    dependency_links=[
        'https://github.com/ionagamed/crawld'
    ]
)

