"""setup."""
import setuptools

setuptools.setup(
    name="duckduckgo_images_api3",
    version="0.1.1",
    url="https://github.com/mpdev10/duckduckgo-images-api",
    author="mpdev10",
    description="DuckDuckGo Image Search Resuts",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="duckduckgo image api python3",
    license="MIT",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['requests>=2.18.4',],
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', 'flake8>=3.3.0', 'tox>=2.7.0', 'vcrpy>=1.11.1'],
    extras_require={
        'packaging': ['setuptools>=38.6.0', 'twine>=1.11.0',],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    #  entry_points={'console_scripts': []},
)
