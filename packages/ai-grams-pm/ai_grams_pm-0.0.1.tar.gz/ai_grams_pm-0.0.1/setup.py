from setuptools import setup

setup(
    name='ai_grams_pm',
    version='0.0.1',    
    description='AI Grams\' API manager for PM',
    author='Antonio Briola',
    author_email='aigrams.team@gmail.com',
    url = 'https://github.com/AIGrams/ai_grams_pm',
    download_url = 'https://github.com/AIGrams/ai_grams_pm/archive/v0.0.1.tar.gz',
    license='MIT',
    packages=['ai_grams_pm'],
    install_requires=[
        'numpy', 'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)