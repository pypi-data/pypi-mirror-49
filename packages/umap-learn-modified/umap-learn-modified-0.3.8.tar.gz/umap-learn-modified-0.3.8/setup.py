from setuptools import setup

def readme():
    with open('README.rst') as readme_file:
        return readme_file.read()

configuration = {
    'name' : 'umap-learn-modified',
    'version': '0.3.8',
    'description' : 'Forked from umap-learn (https://github.com/lmcinnes/umap). Change API so that UMAP accepts precomputed KNN input, rather than always calculating by itself. Remove numba.njit parallel option to avoid delay in the cloud.',
    'long_description' : readme(),
    'classifiers' : [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    'keywords' : 'dimension reduction t-sne manifold',
    'url' : 'https://github.com/lilab-bcb/umap',
    'maintainer' : 'Bo Li',
    'maintainer_email' : 'bli28@mgh.harvard.edu',
    'license' : 'BSD',
    'packages' : ['umap'],
    'install_requires': ['numpy >= 1.13',
                         'scikit-learn >= 0.16',
                          'scipy >= 0.19',
                         'numba >= 0.37'],
    'ext_modules' : [],
    'cmdclass' : {},
    'test_suite' : 'nose.collector',
    'tests_require' : ['nose'],
    'data_files' : ()
    }

setup(**configuration)
