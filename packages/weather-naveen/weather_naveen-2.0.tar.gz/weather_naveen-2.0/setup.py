from distutils.core import setup

setup(
    name='weather_naveen',
    packages=['weather_naveen'],
    version='2.0',
    liscence='MIT',
    description='Weather Forcasting Data',
    author='Naveen Kaushal',
    author_email='pythonlearning.naveen@gmail.com',
    url='https://www.python.org/',
    keywords=['weather_naveen','forcast','openweather'],
    install_requires=[
        'requests'
    ],
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Console',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Operating System :: MacOS :: MacOS X',
      'Operating System :: Microsoft :: Windows',
      'Topic :: Software Development :: Bug Tracking',
    ],
)