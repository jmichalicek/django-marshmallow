from setuptools import setup, find_packages

package_data = []
dependencies = []
setup(name="django_marshmallow",
      version="0.0.1",
      description="Basic Django model serializer subclasses for Marshmallow",
      author="Justin Michalicek",
      author_email="jmichalicek@gmail.com",
      license="www.opensource.org/licenses/bsd-license.php",
      packages=find_packages(),
      package_data={'django_marshmallow' : package_data },
      install_requires=dependencies,
      long_description='Basic Django model serializer subclasses for Marshmallow',
      test_suite='tests')
