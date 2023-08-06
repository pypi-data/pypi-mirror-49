# DrCompare
DrCompare is a python package to compare a list of image pairs. The input is provided as a csv file and, it produces a separate csv file with additional fields.

## Usage
The project is delivered as python package and officially supports linux, macos and windows. You can use standard pip install command to install the package in your environment.
```
pip3 install drcompare
```
Link to pypl : https://pypi.org/project/drcompare/
### Sample Code
```
# On Windows
>>> import drcompare
# Paths on windows are required to be escaped
>>> outputfile = drcompare.drcompare_main("C:\\path\\to\\input\\csv\\file.csv", "C:\\path\\to\\directory\\with\\all\\to\\process")
2019-07-17 03:14:57,223 - main.py - INFO - Absolute output path: C:\path\to\directory\with\all\to\process/output.csv
2019-07-17 03:14:57,239 - main.py - INFO - Input path: C:\path\to\input\csv\file.csv
2019-07-17 03:14:57,270 - main.py - WARNING - The images pair appears to be pointing to the same file : (1) C:\path\to\directory\with\all\to\process/dragon1.jpg; (2) C:\path\to\directory\with\all\to\process/dragon1.jpg
2019-07-17 03:14:57,333 - main.py - WARNING - Found invalid file path(s) in input csv row :['hello how are you', 'I am good']
>>> print(outputfile)
C:\path\to\directory\with\all\to\process/output.csv
```
#### Take away
1. First argument is absolute path to the input csv file.
2. All images pointed in the input csv should kept kept under on directory. The second argument is the absolute path to the directory where all images are kept. The output file shall also be generated in the same image directory.
3. Paths on windows needs to be escaped.
4. For more detail on input and output csv refer Feature-specs. 

Before using the project, consider going through the [Feature Specs](https://github.com/ravjotsingh9/DrCompare/blob/master/docs/Feature-spec.md#drcompare-feature-specs).

## Run it from the code
1. Make sure that pip3 and python3 are installed. The current build is verified on pip3 19.1.1 and python 3.7.
2. Clone the repository.
3. CD into the project.
```
cd drcompare
```
4. Install the dependencies.
```
make deps
```
5. Now, you are all set to run the tests. The test data is provided under image directory. Run following command to run the unitests.
```
make test
```
6. Running from the commadline is similar to as explained in above [Sample Code](#Sample-Code)
```
$ python3 ./drcompare/main.py -h
usage: main.py [-h] --file FILE --dir DIR

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Absolute path to input containing images file names in
                        csv format
  --dir DIR, -d DIR     Absolute path to image directory contaning all images

$ python3 ./drcompare/main.py -f /absolute/path/to/input/csv/input.csv -d /absolute/path/to/directory/where/all/images/to/be/processed/are/kept
...
```


# References:
Some ideas, code and knownledge has been used from the below tutorial:
https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/