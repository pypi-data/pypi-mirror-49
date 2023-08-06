import pathlib
from setuptools import find_packages, setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
	name = 'nanome-matryx',
	packages=find_packages(),
	version = '0.0.1',
	license='MIT',
	description = 'Nanome Plugin to interface with the Matryx Platform',
	long_description = README,
    long_description_content_type = "text/markdown",
	author = 'Nanome',
	author_email = 'hello@nanome.ai',
	url = 'https://github.com/nanome-ai/plugin-matryx',
	platforms="any",
	keywords = ['virtual-reality', 'chemistry', 'python', 'api', 'plugin', 'blockchain', 'matryx'],
	install_requires=['nanome'],
	entry_points={"console_scripts": ["nanome-matryx = nanome_matryx.Matryx:main"]},
	classifiers=[
		'Development Status :: 3 - Alpha',

		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering :: Chemistry',

		'License :: OSI Approved :: MIT License',

		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	],
	package_data={
        "nanome_matryx": [
            "components/*",
            "components/json/*",
            "images/*",
            "menus/*",
            "menus/json/*",
            "menus/json/select_winners/*",
            "menus/select_winners/*",
            "contracts/*",
        ]
	},
)