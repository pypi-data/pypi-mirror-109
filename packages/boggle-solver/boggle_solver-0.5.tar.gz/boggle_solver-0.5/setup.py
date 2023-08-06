from distutils.core import setup
setup(
  name = 'boggle_solver',         # How you named your package folder (MyLib)
  packages = ['boggle_solver'],   # Chose the same as "name"
  version = '0.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A package for auto-generating the possible combinations of a boggle grid.',   # Give a short description about your library
  author = 'Euan Campbell',                   # Type in your name
  author_email = 'dev@euan.app',      # Type in your E-Mail
  url = 'https://github.com/euanacampbell/boggle_solver',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/euanacampbell/boggle_solver/archive/refs/heads/master.tar.gz',    # I explain this later on
  keywords = ['boggle', 'puzzle', 'recursive'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)