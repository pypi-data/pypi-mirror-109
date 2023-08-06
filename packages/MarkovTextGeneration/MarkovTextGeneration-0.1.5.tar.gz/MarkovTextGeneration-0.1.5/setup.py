from setuptools import setup

setup(
    name='MarkovTextGeneration',
    version='0.1.5',    
    description='Generating hallucinated text with Markov Chains',
    long_description="Read the wiki at https://github.com/Sam-Nielsen-Dot/MarkovTextGeneration/wiki",
    url='https://github.com/Sam-Nielsen-Dot/MarkovTextGeneration',
    author='Sam Nielsen',
    author_email='lenssimane@gmail.com',
    license='MIT',
    packages=['MarkovTextGeneration'],
    install_requires=['markovify>=0.9.0',
                    'nltk>=3.5',
                    'spacy>=3.0.6'                  
                      ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Win32 (MS Windows)',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
