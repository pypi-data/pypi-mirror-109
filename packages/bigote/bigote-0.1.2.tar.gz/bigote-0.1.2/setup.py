"""Setup file for bigote."""


from setuptools import setup  # type: ignore


setup(
    author_email="cganterh@gmail.com",
    author="Cristóbal Ganter",
    name="bigote",
    py_modules=["bigote"],
    setup_requires=["setuptools_scm"],
    url="https://github.com/cganterh/bigote",
    use_scm_version=True,
)
