from distutils.core import setup

setup(
  name = 'aivision',         # How you named your package folder (MyLib)
  packages = ['aivision'],   # Chose the same as "name"
  version = '1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This package will help yuo to build many cv projects',
  long_description="aivision is a computer vision package that helps you to build variety of computer vision projects. "
                   "For more info see the github page "
                   "https://github.com/chinmay18030/aivision",
  author = 'Ace Tech Academy',                   # Type in your name
  author_email = 'aceteachacademy@gmail.com',      # Type in your E-Mail
  keywords = ['FaceMesh', 'hand tracking','pose tracking',"virtual background","whole body track"],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'opencv-python',
          'mediapipe',
          "numpy",
          "pyzbar"
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)