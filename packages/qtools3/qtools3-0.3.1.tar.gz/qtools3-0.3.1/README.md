# `qtools3` - Questionnaire Tools for ODK

This software `qtools3` provides tools and utilities for dealing with PMA 
questionnaires. It converts the XLSForms to XML and then does all appropriate 
edits. It also can be used as a simple XLSForm Offline converter.

The software `qtools3` is an upgrade from 
[`qtools2`][qtools2]. The primary purpose for this 
upgrade is to port the software from Python 2 to Python 3. This was made 
possible because the [community's PyXForm][pyxform]
added Python 3 support in 2018.

[qtools2]: https://github.com/jkpr/QTools2
[pyxform]: https://github.com/XLSForm/pyxform

## Pre-requisites

The software `qtools3` relies on Python 3 for core functionality and Java for
ODKValidate. The steps to install are

* Install the most recent version of the [Java JRE][jre].
* Install [Python 3.6][python] or higher.

Note: the author uses [Homebrew][brew] for Python installation on Mac.

[jre]: http://www.oracle.com/technetwork/java/javase/downloads/index.html
[python]: http://www.python.org/downloads/
[brew]: http://brew.sh/

## Windows-specific steps

Some difficulties arise if `python` and `pip` are not be added automatically 
to the `PATH` upon installation. For instructions on how to do this, consult
[this document][path].

[path]: https://www.dropbox.com/s/01uoge5pt7yz0ti/Python%20for%20Windows%20Users.docx?dl=0

Open `CMD` (click start menu, type `CMD`, press enter).

```
cd C:\Python36\Scripts
```

Continue with installation or upgrade...

## Installation

NOTE: Windows users start with the _**Windows-specifc steps**_ section.

On a terminal or CMD, run

```
python3 -m pip install qtools3
```

For the latest and greatest, install directly from github

```
python3 -m pip install https://github.com/PMA-2020/qtools3/zipball/master
```


## Command-line usage

Besides being the workhorse of `qtools3`, the module `qtools3.convert` also provides a command-line utility. New-style linking (with all instructions contained inside the XLSForm) is now the default. Old-style linking (line-by-line manual XML editing instructions) is removed. To see help files and usage, run in the terminal

```
python -m qtools3.convert --help
```

#### Quick-start guide

| Type of conversion | Command |
| ------------------ | ------- |
| PMA form conversion                                   | `python -m qtools3.convert FILENAME [FILENAME ...]`    |
| XLSForm-Offline equivalent, convert and validate      | `python -m qtools3.convert -ril FILENAME [FILENAME ...]`     |

#### Options
| Short Flag | Long Flag | Description |
| --- | --- | --- |
| -r | --regular | This flag indicates the program should convert to XForm and not try to enforce PMA-specific naming conventions or make linking checks for HQ and FQ. |
| -p | --preexisting | Include this flag to prevent overwriting pre-existing files. |
| -n | --novalidate | Do not validate XML output with ODK Validate. Do not perform extra checks on (1) data in undefined columns, (2) out of order variable references. |
| -i | --ignore_version | Ignore versioning in filename, form_id, form_title, and save_form. In other words, the default (without this flag) is to ensure version consistency. |
| -l | --linking_warn | Produce warnings for incorrect linking directives. Default is to raise an exception and halt the program. |
| -d | --debug | Show debug information. Helpful for squashing bugs. |
| -e | --extras | Perform extra checks on (1) data in undefined columns and (2) out of order variable references. |
| -s | --suffix | A suffix to add to the base file name. Cannot start with a hyphen ("-"). |

## Extras

### Translation Regex Mismatches
These `qtools3` conversion warning messages appear whenever there is a discrepancy between translations with respect to numbering, i.e. `'[0-9]+'`, and/or variables, i.e. `'${...}'`.

*Example - Numbering Mismatch*

In this example, the warning `'[0-9]+'` will appear, because "0" is not the same things as "zero". To fix this, please ensure that ALL languages use only arabic numerals (e.g. 1, 2, 3...), or only word-based numbering (e.g. one, two, three...).
  * English: Please enter 0.
  * Bad Pidgin English: Please enter zero.

*Example - Variable Mismatch*

ODK variables should never be translated. If the main language shows "${months}", all language translations should also show "${months}". Of course, what the user sees on the phone will still be translated.
  * English: Enter ${months}.
  * Bad French: Entrez ${mois}.

*Example - Variable Mismatch*

Translations should use all variables that the English uses.
  * English: There are ${hh_count} people in the household
  * Bad Pidgin English: There are (ODK will fill in a count) people in the household

## Updates

NOTE: Windows users start with the _**Windows-specifc steps**_ section. To install `qtools3` updates, use

```
python3 -m pip install qtools3 --upgrade
```

For the latest and greatest, replace `master` in the URLs above with `develop`.

Every once in a while, it will be necessary to update `pmaxform3`. To do this, use

```
python3 -m pip install pmaxform3 --upgrade
```

# Suggestions and Gotchas

- Check the version in the terminal to see if a program is installed.
- Check Java version with `javac -version`
- Check Python version with `python -V`.
- Check pip version with `pip -V`.
- Another executable for Python is `python3`.
- Another executable for `pip` is `pip3`.
- The most recent Java is not required, but successful tests have only been run with Java 1.6 through Java 1.8.
- A dependency of `pmaxform` is `lxml`, which can cause problems on Mac. If there are problems, the best guide is on [StackOverflow][8].
- During installation of `pmaxform` on Mac, the user may be prompted to install Xcode's Command Line Tools. This should be enough for `lxml`.
- `qtools3` may run without Java. Java is only needed for ODK Validate, which can be bypassed by using the "No validate" option.
- Xcode 9 presents issues with missing header files. If at all possible, install Xcode 8.

[8]: http://stackoverflow.com/questions/19548011/cannot-install-lxml-on-mac-os-x-10-9
