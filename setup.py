from setuptools import setup

setup(name='ISS Tracker',
      version='0.1',
      description='Tool that tells you when the ISS is next due to pass over a given location',
      url='https://github.com/covertbert/ISS-next-pass',
      author='Bertie Blackman',
      author_email='blackmanrgh@gmail.com',
      license='MIT',
      install_requires=[
          'geopy',
      ],
      zip_safe=False)
