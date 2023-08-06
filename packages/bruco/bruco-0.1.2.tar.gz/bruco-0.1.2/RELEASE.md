To cut a new release

- update version number in
    - `/bruco/__init__.py`
    - `/bruco.spec`
- update dependencies in
    - `/setup.py`
    - `/bruco.spec`
    - `/debian/control`
- add changelog entries in
    - `/bruco.spec`
    - `/debian/changelog`
- commit the new release
- git tag the repo at this point
- create a new tarball:

  ```
  python setup.py sdist
  ```

- upload the new tarball to software.ligo.org and pypi.python.org
