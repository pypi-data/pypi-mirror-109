[![CI][ci:b]][ci]
[![License MIT][license:b]][license]
![Python3.8][python:b]
[![pypi][pypi:b]][pypi]
[![codecov][codecov:b]][codecov]

[ci]: https://github.com/perellonieto/DiaryPy/actions/workflows/ci.yml
[ci:b]: https://github.com/perellonieto/diarypy/workflows/CI/badge.svg
[license]: https://github.com/perellonieto/DiaryPy/blob/master/LICENSE.txt
[license:b]: https://img.shields.io/github/license/perellonieto/diarypy.svg
[python:b]: https://img.shields.io/badge/python-3.8-blue
[pypi]: https://badge.fury.io/py/diarypy
[pypi:b]: https://badge.fury.io/py/diarypy.svg
[codecov]: https://codecov.io/gh/perellonieto/DiaryPy
[codecov:b]: https://codecov.io/gh/perellonieto/DiaryPy/branch/master/graph/badge.svg?token=AYMZPLELT3


# DiaryPy

### A python class to automatically save the partial/intermediary results of a running experiment in a set of notebooks (csv files) and images as files.

[![Build Status](https://travis-ci.org/perellonieto/DiaryPy.svg?branch=master)](https://travis-ci.org/perellonieto/DiaryPy)

Create a new diary

```
from diarypy.diary import Diary
diary = Diary(name='world', path='hello', overwrite=False,
              stdout=False, stderr=False)
```

Create all the notebooks that you want to use

```
diary.add_notebook('validation')
# You can use the returned instance later
notebook_test = diary.add_notebook('test')
# And specify the header
notebook_train = diary.add_notebook('training', header=['iteration', 'accuracy'])
```

Store your results in the different notebooks

```
diary.add_entry('validation', ['accuracy', 0.3])
diary.add_entry('validation', ['accuracy', 0.5])
diary.add_entry('validation', ['accuracy', 0.9])
notebook_train.add_entry([0, 0.4])
notebook_train.add_entry([1, 0.6])
notebook_train.add_entry([2, 0.8])
notebook_test.add_entry(['First test went wrong', 0.345, 'label_1'])
```

Add an image

```
from PIL import Image
image = Image.new(mode="1", size=(16,16), color=0)
diary.save_image(image, filename='test_results')
```

### Resulting files

The files that are generated after executing the previous lines are

```
hello/
└── world
    ├── description.txt
    ├── images
    │   └── test_results_4.png
    ├── test.csv
    └── training.csv
    └── validation.csv
```
the content of the files is

description.txt
```
Date: 2015-10-22 17:43:19.764797
Name : world
Path : hello/world
Overwrite : False
Image_format : png
```

validation.csv
```
1,1,|2021-06-17|,|12:56:45.945000|,|accuracy|,0.3
2,2,|2021-06-17|,|12:56:46.813717|,|accuracy|,0.5
3,3,|2021-06-17|,|12:56:53.358989|,|accuracy|,0.9
```

training.csv
```
|id1|,|id2|,|date|,|time|,|iteration|,|accuracy|
4,1,|2021-06-17|,|12:56:54.231691|,0,0.4
5,2,|2021-06-17|,|12:56:55.128130|,1,0.6
6,3,|2021-06-17|,|12:56:56.006014|,2,0.8
```

test.csv
```
7,1,|2021-06-17|,|12:56:56.761961|,|First test went wrong|,0.345,|label_1|
```

# Unittest

```
python -m unittest discover diarypy
```
