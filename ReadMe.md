# Headcount sheet automation

This project automates filling out part of the headcount sheets for the Champions program at Eliot Upper.

The script can fill out all the sheets for 1 week.

## How to use:

1. Install dependencies
2. Replace text file contents
3. Run Python script

# Install dependencies:

To run the code, you must first install some libraries that the code relies on. In the command line, run the following commands:

`pip install xlwt`

`pip install numpy`

If you are using the newer version of Python (Python 3), replace `pip` with `pip3`.

## Replace text file contents:

To generate headcount sheets for the week, you need to update the text file that stores all the data. This is found in `headcount_data.txt`.

If you look in `headcount_data.txt`, you'll see a horizontal line `===================` near the top. Above all this line, you need to copy and paste the daily totals in the format `Wednesday: 48`.

Below this, you can copy and paste everything from the table sent in the weekly email, straight as it is.

If you need an example of how to format the entire file, look at (example_data_format.txt)[https://github.com/ljiang09/example_data_format.txt].

## Run Python script

Now, you can finally run the python script and generate Excel files for each day. In the command line, navigate to the folder where this ReadMe file is stored. Then, type `python main.py` and press enter, and see the newly-generated Excel sheets!
