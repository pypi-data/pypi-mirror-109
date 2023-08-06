from setuptools import setup, find_packages

setup(
    name='apievaluator',
    author='Filip Majetić',
    author_email='filip.majetic@fer.hr',
    version='0.0.3',
    description='Validate an API specification and run tests',
    keywords=['rest', 'api', 'testing', 'automated'],
    url='https://gitlab.com/fmajestic/api-evaluator',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['click',
                      'prance',
                      'pyyaml',
                      'requests',
                      ],
    entry_points={
        'console_scripts': ['apieval=apievaluator.main:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
