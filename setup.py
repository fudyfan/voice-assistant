from setuptools import setup, find_packages

setup(
    name="voice-assistant",
    version='0.1',
    # py_modules=['main', 'low_pass_filter', 'time_stretch'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    install_requires=[
        'wheel',
        'Click',
        'librosa'
    ],
    entry_points={
        'console_scripts': [
            'process=main:main',
        ],
    },

)
