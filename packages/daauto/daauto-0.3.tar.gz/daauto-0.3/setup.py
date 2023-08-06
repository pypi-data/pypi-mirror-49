from setuptools import setup

setup(name='daauto',
      version='0.3',
      description='autodata',
        classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      url='https://github.com/AronWater/daauto',
      author='AronWater2',
      author_email='kclukac@connect.ust.hk',
      license='MIT',
      packages=['daauto'],
       install_requires=[
          'markdown',
      ],
      zip_safe=False)