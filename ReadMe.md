# Headcount sheet automation

This project automates filling out part of the headcount sheets for the Champions program at Eliot Upper.

The script can fill out all the sheets for 1 week. It generates two files: one for Pre-K and one for Grade school kids. Each file has a sheet for each day.

## How to use:

1. Download project
2. Install dependencies
3. Replace text file contents
4. Run Python script
5. Optional: run unit tests


## Download project:

Go to [https://github.com/ljiang09/headcount](https://github.com/ljiang09/headcount). In the top right ish of the screen, click the green "Code" button to show a drop down menu. In this drop down, click "Download ZIP". Once downloaded, unzip into your computer.


## Install dependencies:

To run the code, you must first install some libraries that the code relies on. In the command line, run the following commands:

`pip install xlwt`

`pip install numpy`

`pip install pillow`

If you are using the newer version of Python (Python 3), replace `pip` with `pip3`.


## Replace text file contents:

To generate headcount sheets for the week, you need to update the text file that stores all the data. This is found in [`headcount_data.txt`](https://github.com/ljiang09/headcount/blob/main/headcount_data.txt).

If you look in [`headcount_data.txt`](https://github.com/ljiang09/headcount/blob/main/headcount_data.txt), you'll see a horizontal line `===================` near the top. Above this line, you need to state the date of the week's Sunday. This should be in the format `mm/dd/yy`.

There is a second horizontal line. Above this line, you need to copy and paste the daily totals in the format `Wednesday: 48`. Each day gets its own line.

Below this, you can copy and paste everything from the table sent in the weekly email, straight as it is.

If you need an example of how to format the entire file, look at [`example_data_format.txt`](https://github.com/ljiang09/example_data_format.txt).


## Run Python script

Now, you can finally run the python script and generate Excel files for each day. In the command line, navigate to the folder where this ReadMe file is stored. Then, type either `python main.py` or `python3 main.py`, press enter, and see the newly-generated Excel sheets!


## Optional: run unit tests

I've written tests to check that the script is functioning as intended. If you want to, you can run these yourself! You'll need to install `pytest`, then in the command line, run the command `pytest`. You should then see all the functions being tested, and which ones pass or fail.

