# Books

This program is for converting an audiobook into pages read.

## Usage

To use this program, you must have Python 3.6 or higher installed. You must then install the
requirements. It's recommended you do this under a virtual environment.

```
pip install .
```

Run the program under Python as a module. Arguments to be supplied are:

* -c, --completed: How much of the audiobook have you completed.
* -o, --overall: How long is the audiobook overall.
* -p, --pages: How many pages is the print book overall.

```
audio2book -c 0:53 -o 10:58 -p 310
```

You can also use the long arguments.

```
audio2book --completed --overall 10:58 -p 310
```

And you can get help.

```
audio2book -h
```

## Development

A contribution guide is coming.

### Running the tests

Make sure you have first installed the requirements:

```
pip install -r requirements.txt
```

Then run the tests.

```
./test.sh
```

The tests include unit tests and mutation tests. All new functionality must have 100% test
coverage and provide any useful logging. Any reasonable exceptions to this will be considered.
