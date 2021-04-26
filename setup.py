from setuptools import setup

setup(name='idcard_generator',
      version='22',
      description='idcard_generator',
      author='airobot',
      author_email='airobot@airobot.link',
      license='GPL-3.0',
      packages=['idcard_generator'],
      # data_files=['idcard_generator/asserts/empty.png', 'idcard_generator/asserts/fzhei.ttf', 'idcard_generator/asserts/hei.ttf', 'idcard_generator/asserts/ico.icns', 'idcard_generator/asserts/ocrb10bt.ttf'],
      include_package_data=True,
      install_requires=['numpy', 'pillow', 'opencv-python']
      )
