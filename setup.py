from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='BacGenomePipeline',
    version='1.0',
    description='Complete Bacterial Genome Assembly and Annotation Pipeline',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/StephenFordham/BacGenomePipeline',
    author='Stephen Fordham',
    author_email='sfstephenfordham@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['Genome Assembly', 'WGS', 'bacterial pipeline', 'prokaryotic', 'bacterial genome assembly'],
    packages=find_packages(),
    install_requires=['medaka==1.2.1', 'NanoStat==1.5.0', 'staramr==0.7.2', 'numpy==1.19.5', 'scipy==1.4.1'],
    entry_points={
        'console_scripts': [
            "BacGenomePipeline = BacGenomePipeline.BacGenomePipeline:main",
        ]}
    )
