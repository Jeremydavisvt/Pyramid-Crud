from setuptools import setup, find_packages

setup(name='crud',
      version='0.0',
      description='pyramid crud web app',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='untitled1',
      install_requires=[
          'pyramid',
          'pyramid_chameleon',
          'pyramid_debugtoolbar',
          'pyramid_tm',
          'SQLAlchemy',
          'transaction',
          'zope.sqlalchemy',
          'waitress', 'bcrypt==2.0',
      ],
      entry_points="""\
      [paste.app_factory]
      main = crud:main
      """,
      )
