from setuptools import setup, find_packages

setup(
    name='pyorganizer',
    version='0.0.1',
    install_requires=[
        'requests',
        'importlib-metadata; python_version<"3.10"',
        "pywin32 >= 1.0;platform_system=='Windows'",
    ],
    include_package_data=True,
    package_dir = {"": "src"},
    packages=find_packages(where="src"),
    entry_points = {
        "console_scripts" : [
            "py-organize = cli:main" 
        ]
    }
)