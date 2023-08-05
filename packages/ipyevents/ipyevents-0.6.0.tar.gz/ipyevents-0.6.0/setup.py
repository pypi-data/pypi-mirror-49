from os.path import join as pjoin

from setupbase import (
    create_cmdclass, install_npm, ensure_targets,
    find_packages, combine_commands, ensure_python,
    get_version, HERE
)

from setuptools import setup

LONG_DESCRIPTION = 'A custom widget for returning mouse and keyboard events to Python'

# The name of the project
name = 'ipyevents'

# Ensure a valid python version
ensure_python('>=3.5')

# Get our version
version = get_version(pjoin(name, '_version.py'))

nb_path = pjoin(HERE, name, 'nbextension', 'static')
lab_path = pjoin(HERE, name, 'labextension')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, 'index.js'),
    pjoin(HERE, 'lib', 'plugin.js'),
]

package_data_spec = {
    name: [
        'nbextension/static/*.*js*',
        'labextension/*.tgz'
    ]
}

data_files_spec = [
    ('share/jupyter/nbextensions/ipyevents',
        nb_path, '*.js*'),
    ('share/jupyter/lab/extensions', lab_path, '*.tgz'),
    ('etc/jupyter/nbconfig/notebook.d', HERE, 'ipyevents.json')
]


cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
                           data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(HERE, build_cmd='build:all'),
    ensure_targets(jstargets),
)

setup_args = dict(
    name            = name,
    description     = 'A custom widget for returning mouse and keyboard events to Python',
    version         = version,
    cmdclass        = cmdclass,
    packages        = find_packages(),
    author          = 'Matt Craig',
    author_email    = 'mattwcraig@gmail.com',
    url             = 'https://github.com/mwcraig/ipyevents',
    license         = 'BSD 3-clause',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Jupyter', 'Widgets', 'IPython'],
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Jupyter',
    ],
    include_package_data = True,
    install_requires = [
        'ipywidgets>=7.0.0',
    ],
    extras_require = {
        'test': [
            'pytest',
            'pytest-cov',
            'nbval',
        ],
        'docs': [
            'sphinx>=1.5',
            'recommonmark',
            'sphinx_rtd_theme',
            'nbsphinx>=0.2.13,<0.4.0',
            'jupyter_sphinx',
            'nbsphinx-link',
            'pytest_check_links',
            'pypandoc',
        ],
    },
)

# setup_args = {
#     'name': 'ipyevents',
#     'version': version_ns['__version__'],
#     'description': 'A custom widget for returning mouse and keyboard events to Python',
#     'long_description': LONG_DESCRIPTION,
#     'license': 'BSD 3-clause',
#     'include_package_data': True,
#     'data_files': [
#         ('share/jupyter/nbextensions/ipyevents', [
#             'ipyevents/static/extension.js',
#             'ipyevents/static/index.js',
#             'ipyevents/static/index.js.map',
#         ]),
#         ('etc/jupyter/nbconfig/notebook.d', [
#             'jupyter.d/notebook.d/ipyevents.json'
#         ]),
#     ],
#     'install_requires': [
#         'ipywidgets>=7.0.0',
#     ],
#     'packages': find_packages(),
#     'zip_safe': False,
#     'cmdclass': {
#         'build_py': js_prerelease(build_py),
#         'egg_info': js_prerelease(egg_info),
#         'sdist': js_prerelease(sdist, strict=True),
#         'jsdeps': NPM,
#     },

#     'author': 'Matt Craig',
#     'author_email': 'mattwcraig@gmail.com',
#     'url': 'https://github.com/mwcraig/ipyevents',
#     'keywords': [
#         'ipython',
#         'jupyter',
#         'widgets',
#     ],
#     'classifiers': [
#         'Development Status :: 4 - Beta',
#         'Framework :: IPython',
#         'Intended Audience :: Developers',
#         'Intended Audience :: Science/Research',
#         'Topic :: Multimedia :: Graphics',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.3',
#         'Programming Language :: Python :: 3.4',
#         'Programming Language :: Python :: 3.5',
#     ],
# }

if __name__ == "__main__":
    setup(**setup_args)
