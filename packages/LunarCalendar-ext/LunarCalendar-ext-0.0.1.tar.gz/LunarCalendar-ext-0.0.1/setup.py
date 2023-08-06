from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='LunarCalendar-ext',
    version='0.0.1',
    description='A fork from LunarCalendar.',
    long_description=long_description,
    author='KaixuYang',
    author_email='kaixuyang@gmail.com',
    url='https://github.com/KaixuYang/LunarCalendar-extension',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'python-dateutil>=2.6.1',
        'ephem>=3.7.5.3',
        'pytz',
    ],
    python_requires='>=2.7, <4',
    entry_points={
        'console_scripts': [
            'lunar-find=lunarcalendar.command:find',
        ],
    },
)
