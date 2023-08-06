from distutils.core import setup
setup(
  name = 'PyJ2L',         # How you named your package folder (MyLib)
  packages = ['PyJ2L'],   # Chose the same as "name"
  version = '1.0.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Easy Module to Create Apps',   # Give a short description about your library
  author = 'PyJ2L',                   # Type in your name
  author_email = 'pypyvid@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Computervision', 'Projects', 'HandTracking','FaceRecognition','OpenCV','GUI'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'opencv-python',
          'numpy',
          'autopy',
          'mediapipe',
          'pycaw',
          'cvzone',
          'face_recognition',
          'tkcalendar',
          'keras',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.6',
  ],
)