from distutils.core import setup

setup(
    name='githubRawExtractor',  # How you named your package folder (MyLib)
    packages=['githubRawExtractor'],  # Chose the same as "name"
    version='0.1.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='This package will help you to extract github raw content easily easily',
    long_description="This package will help you to extract text from github raw files, execute it and save it. For "
                     "example see https://github.com/chinmay18030/githubRawExtractor",
    author='Ace Tech Academy',  # Type in your name
    author_email='aceteachacademy@gmail.com',  # Type in your E-Mail

    install_requires=[  # I get to this in a second
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.6',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
