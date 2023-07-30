# mystatements 💰🪙

Process and analyze your TD Financial statements in bulk and generate useful insights from your spending history. The name is a play on the TD's personal finance app of a similar name, myspend.

**NOTE:** this project only _processes_ your statement data and stores it in a local SQLite instance. It _does not_ store your financial data on servers.

## About

The goal of this project is to produce app to understand my long-term spending behaviours through analyzing TD statements. There is no easy way to access your spending data from myspend, Mint, etc., but your statements do contain this information.

It acts as a kind of addition to TD myspend; where myspend is useful for tracking your transactions as they happen, mystatements provides you with a better picture of your past spending habits, and provides an easier interface for predicting future spending (e.g., tracking subscriptions, consistent purchases, etc).

Another major motivation for this project is that I find myspend a bit buggy and think Mint isn't the perfect solution for my needs.

## Roadmap

- [ ] Process savings and chequing accounts
- [ ] Clean up line-by-line code for savings and chequing
- [ ] Add support for subscriptions
- [ ] Add support for graphs (i.e., use matplotlib)
- [ ] Upload your statement, host on web-server
- [ ] Write a guide to commands/API for transaction.py

## Setup

Firstly, you need Python (with version >= 3), pip, and Java (for [Apache Tika](https://tika.apache.org/)) installed. For Tika, [you need Java 7+](https://github.com/chrismattmann/tika-python); Java 8 is recommended.

```sh
# for Python, use homebrew: https://docs.brew.sh/Installation
brew install python
$ python --version
> Python 3.9.5

# for Java, use SDKMAN! https://sdkman.io/install
sdk install java 8.292.10.1-amzn
$ java -version
> openjdk version "1.8.0_292"
> OpenJDK Runtime Environment Corretto-8.292.10.1 (build 1.8.0_292-b10)
> OpenJDK 64-Bit Server VM Corretto-8.292.10.1 (build 25.292-b10, mixed mode)
```

You'll need to create a virtual environment. On Linux, do the following

```sh
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
deactivate # only when you need to, of course
pip install -r requirements.txt # to install dependencies
pip freeze > requirements.txt # to save updated dependencies
```

Then you'll need to add your bank statements to `data/statements` and your account information to `data/accounts`. After that, try

```sh
python src/filename.py # normalizes statement filenames
python src/accounts.py [chequing|savings] # processes account CSV data
python src/accounts.py [chequing|savings] # processes statement PDF data
```

## Files

```bash
├── README.md # This file!
├── data
│   └── accounts # A folder for recent account summaries from TD
│       └─── your_accounts_go_here.csv
│   ├── chequing.json # A file with all known data that can appear in a chequing statement
│   ├── savings.json # A file with all known data that can appear in a savings statement
│   └── statements # A folder for all chequing and savings statements from TD
│       └─── your_statements_go_here.pdf
├── data.py # Add to either chequing.json or savings.json with this tool
├── data_helper.py # Another tool to help you figure out what to input into data.py (if you're stuck)
├── filename.py # Normalize all filenames in /statements; very useful if downloading from TD directly
├── files.sh # A short bash script to generate this tree; run `bash files.sh` to execute
├── reader.py # Process a user's transactions and print summary statistics/graphs; see TRANSACTION.md for more
├── requirements.txt # Python dependencies list
└── transaction.py # The transaction data types used in this project
```

## Usage

### Statements

Normalize filenames by running:

`python filename.py`

Process each month and see a net difference by running:

`python reader.py`

Add data to the chequing/savings statement knowledge bank by running:

`python data.py`

If you're unsure what to input, running this diagnostic will help:

`python data_helper.py`

### Graphs

TODO

## Contributing

This project is actively looking for contributors! Message me at michaelfromyeg@gmail.com if you're interested.
