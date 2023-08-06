from distutils.core import setup
from setuptools import find_packages
from apptrack import __version__


setup(name='AppTrack',
        version=__version__,
        description='''apptrack is a strong application track tool on distributed system ''',
        author='wukan',
        author_email='kan.wu@genetalks.com',
        url='',
        license='Mulan',
        packages=find_packages(),
        install_requires=['opentracing'],
        zip_safe=False,
        package_data={},
        data_files = [],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Programming Language :: Python",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7"
        ],
        keywords = '',
        entry_points="""
        [console_scripts]
        apptrack = apptrack:main
        """
)

