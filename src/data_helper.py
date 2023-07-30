# A script to help users determine what to enter to the savings.py prompts

import os
from pprint import pprint
from tika import parser

STATEMENTS_DIRECTORY = 'statements/'
TEST_VAL = 'SSV FRM'

def savings_helper() -> None:
  for filename in os.listdir(STATEMENTS_DIRECTORY):
    raw = parser.from_file(f"{STATEMENTS_DIRECTORY}/{filename}")
    text = "".join([s for s in raw['content'].strip().splitlines(True) if s.strip("\r\n").strip()]) # raw['content']
    lines = text.split('\n')
    for line in lines:
      if TEST_VAL in line:
        print()
        print('Remember to check for two things:\n\t(1) the number that matches the dollar amount of the transaction itself and\n\t(2) the expression that matches that date (in the form MMDD).')
        print()
        print(f"Original line: {line}")
        values  = line.split(' ')
        for i, v in enumerate(values):
          print('\t', i, v)
        print()
        return None
  print("Test value not found. Are you sure its in your statements?")
  return None

# Driver code
if __name__ == '__main__':
  savings_helper()