from setuptools import setup, find_packages


setup(
    name="hypebot",
    version="0.1.0",
    description=(
        "Prepare for a whole bucket of hype from those that know humans best: computers"
    ),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="hypebot",
    author="Jon Robison",
    author_email="narfman0@gmail.com",
    license="LICENSE",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["python-twitter"],
    test_suite="tests",
    entry_points={
        'console_scripts': [
            'hypebot = hypebot.main:main'
        ],
    },
)
