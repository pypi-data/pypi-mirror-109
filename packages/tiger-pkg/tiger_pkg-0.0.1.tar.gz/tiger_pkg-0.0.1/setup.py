import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

# "name”은 패키지의 이름입니다. 이미 Pypi.org에 등록되어 있는 이름을 사용하지 않아야합니다.
# “version”은 패키지 버전을 의미합니다.
# “author”와 “author_email”은 패키지의 작성자의 정보를 나타냅니다.
# (추후 PyPI에 업로드하였을때 표기되고 문의를 받는 메일주소가 됩니다.)
# “description”은 한 문장정도로 설명할 수 있는 패키지의 요약 정보입니다.
# “long_description”은 패키지의 자세한 설명을 작성합니다. PyPI에 보여지며 보통 README.md를 로드합니다.
# “long_description_content_type”은 “long_description”의 타입을 표기합니다.
# 위 예제의 경우 Markdown을 의미합니다.
# “url”은 프로젝트의 홈페이지 URL을 의미하며 보통 Github를 링크합니다.
# “packages”는 배포 패키지에 포함되어야 하는 Python 패키지를 입력합니다.
# 수동으로 입력할 수도 있고 find_packages()라는 함수를 이용하여
# 자동으로 모든 패키지와 서브 패키지를 찾을 수도 있습니다.
#
# “classifiers”는 패키지에 대한 몇가지 추가적인 메타데이터를 입력합니다.
# setuptools.setup(
#     name="tiger_pkg",
#     version="0.0.1",
#     author="jh.lim",
#     author_email="avein74@gmail.com",
#     description="A small example package",
#     long_description = open('README.md').read(),
#     url="https://github.com/hongi1974/tiger_pkg",
#     packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
# )

setuptools.setup(
    name="tiger_pkg",
    version="0.0.1",
    author="jh.lim",
    author_email="avein74@gmail.com",
    description="A small example package",
    long_description="long_description",
    long_description_content_type="text/markdown",
    url="https://github.com/hongi1974/tiger_pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)