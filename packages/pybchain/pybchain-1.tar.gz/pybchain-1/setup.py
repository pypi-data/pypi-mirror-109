from distutils.core import setup
setup(
  name = 'pybchain',         # How you named your package folder (MyLib)
  packages = ['pybchain'],   # Chose the same as "name"
  version = '1',      # Start with a small number and increase it with every change you make
  license='mit',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Simple blockchain concept package',   # Give a short description about your library
  author = 'unfuz3',                   # Type in your name
  author_email = 'mr.mendozamen@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/unfuz3/pybchain',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/unfuz3/pybchain/archive/refs/tags/v1.tar.gz',
  keywords = ['blockchain', 'python', 'concept'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.9',      #Specify which pyhton versions that you want to support,
  ],
)
