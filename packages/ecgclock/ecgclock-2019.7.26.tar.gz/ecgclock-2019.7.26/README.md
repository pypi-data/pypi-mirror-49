# ECG Clock Plotter #

This repository contains a python library for simple plotting of ECG data (typically QTc values) in the "24 hour clock" format:

![Example QT Clock](https://bitbucket.org/atpage/ecgclock/raw/master/data/example/baseline_vs_drug.png)

### DISCLAIMER: ###

All of the included default values, thresholds/ranges, example data sets, etc. are for illustration, not for diagnostic use.  It is the clinician's responsibility to adjust all settings appropriately.

### How do I get set up? ###

You will need Python 3 with the following modules available:

* [`numpy`](http://www.numpy.org/)
* [`dateutil`](http://labix.org/python-dateutil)
* [`matplotlib`](http://matplotlib.org/)
* [`cycler`](http://matplotlib.org/cycler/)
* [`pandas`](https://pandas.pydata.org/)

Depending on the chosen `matplotlib` backend, there may be other dependencies, such as `PySide`/`PySide2` or `PyGTK`.

To install from PyPI:

    pip3 install ecgclock

Or from git:

    git clone https://bitbucket.org/atpage/ecgclock.git
    cd ecgclock
    pip3 install -e .

### How do I run it? ###

`ECGClock` is the main class that allows you to create and plot an ECG Clock.  It is subclassed as `QTClock`, etc.

There are two main things (classes) that you would want to add to a clock: the `Recording`, and the `Cohort`.  A `Recording` is a set of measurements from a single ECG recording (e.g. a 24-hour Holter).  It will be plotted as a continous line on the clock (see blue and purple lines in the example).  A `Cohort` is a set of `Recordings`, from which you want to plot the typical range of some measured value.  For example, you may want to plot the IQR of QTc in a `Cohort` of healthy adults, to see how it compares to another `Cohort` or individual `Recording`.  The green region in the example was created by plotting one `Cohort` with two different percentile ranges.

The basic process to make a clock, then, is:

1. Create an `ECGClock`.
2. Add 1 or more `Recordings` and/or `Cohorts` to the clock.
3. Configure additional properties of the clock, such as the legend, or highlighting dangerous value ranges.
4. Save the clock as an image file, or show it in an interactive window.

Step 2 may also require some pre-processing, e.g. computing heart rate corrected columns that weren't provided in the original measurements.

For example code, see `test_simple_clock()` and `test_complex_clock()` in `test_ecgclock.py`.

In Windows you should run `multiprocessing.freeze_support()` at the beginning of any `__main__` function.

This package also includes a `make_qtclock` command.  Run `make_qtclock -h` for details.

### Note on API changes: ###

Usage of this library was originally documented in [this article](https://doi.org/10.1109/ACCESS.2015.2509426).  However, significant refactoring of the code is taking place in 2018, including API changes.  The article is still a good reference, but specific code examples will no longer work as-is.

To use the old version of the library, roll back to commit 7e4d4ce (which is tagged as 'old').

### Who do I talk to? ###

* Alex Page, alex.page@rochester.edu
* Jean-Phillippe Couderc, URMC
