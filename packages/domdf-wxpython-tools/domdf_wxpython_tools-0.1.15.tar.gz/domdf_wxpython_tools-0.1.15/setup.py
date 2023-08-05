from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
	name="domdf_wxpython_tools",
	version="0.1.15",
    author='Dominic Davis-Foster',
	author_email="dominic@davis-foster.co.uk",
	packages=find_packages(),
	license="OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
	url="https://github.com/domdfcoding/domdf_wxpython_tools",
	description='Tools and widgets for wxPython',
	long_description=long_description,
	long_description_content_type="text/x-rst",
	classifiers=[
        "Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
		"Development Status :: 4 - Beta",
    ],
	install_requires=[
		"matplotlib>=3.0.0"
	#	"wxPython >= 4.0.0",
	],
)
