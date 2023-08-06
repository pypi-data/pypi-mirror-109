from distutils.core import setup
setup(
  name = 'BasicEmail',
  packages = ['BasicEmail'],
  version = '0.1',
  license='MIT',
  description = 'Wrapping the Main methods, in a class, from the python package smtplib to send a simple email.',
  author = 'John Piper',
  author_email = '',
  url = 'https://github.com/John-Piper',
  download_url = 'https://github.com/John-Piper/BasicEmail/releases/tag/v0.1-alpha',
  keywords = ['email', 'basic', 'smtplib'],
  install_requires=[
          ''
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)