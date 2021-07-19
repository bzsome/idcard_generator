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
      install_requires=['numpy==1.20.3', 'pillow==8.3.1', 'opencv-python==4.5.2.54']
      )
