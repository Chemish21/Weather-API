#Python
import argparse

#Setting top parser
parser = argparse.ArgumentParser()

#Setting arguments
parser.add_argument("-t", "--today", action="store_true", help="get today's weather")
parser.add_argument("-r", "--range", action="store_true", help="get weather between a start/end date. Limit: 31 days")

#Finalizing arguments
arg = parser.parse_args()