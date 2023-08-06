from setuptools import setup, find_packages

setup(
    name             = 'performance_logger',
    version          = '1.0.3',
    description      = 'check performance of the func using decorator',
    author           = 'Sean Kim',
    author_email     = 'ddhyun93@gmail.com',
    url              = '',
    download_url     = '',
    install_requires = ['logger'],
    long_description = open('README.md').read(),
    long_description_content_type='text/markdown',
	include_package_data=True,
	packages=find_packages(),
    keywords         = ['performance_logger'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)