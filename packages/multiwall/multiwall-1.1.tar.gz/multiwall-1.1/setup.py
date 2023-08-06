from setuptools import setup

setup(name='multiwall',
      version='1.1',
      description='Wallpaper Getter and Setter',
      url='https://gitlab.com/avalonparton/multiwall',
      author='Avalon Parton',
      author_email='avalonlee@gmail.com',
      license='MIT',
      packages=['multiwall'],
      install_requires=['Pillow', 'python-unsplash'],
      zip_safe=False)
