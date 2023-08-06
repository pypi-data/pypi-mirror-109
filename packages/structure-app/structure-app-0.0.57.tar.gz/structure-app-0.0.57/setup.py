from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='structure-app',
    version='0.0.57',
    description='create skeleton for framework falcon, fastApi',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Luis Meza',
    author_email='luis@luis.com',
    license='MIT',
    url='https://gitlab.com/Luisff3rnando/code_generators/-/tree/staging/',
    platforms=['Any'],
    py_modules=[],
    install_requires=['setuptools'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    entry_points={
        "console_scripts": [
            "structure_app = structure_app.__main__:main"
        ]
    },
    python_requires='>=3'
)
