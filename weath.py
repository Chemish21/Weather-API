#!/usr/bin/env python3
import api
from args import arg

def main():
  
  #Displaying usage information and getting location
  print("Location Format: [1] Zip Code or [2] City,Nation")
  print("Example: 12345 or London,UK")
  print("-------------------------------------------------")
  location = input("Enter location: ")
  print()

  #Run task based on option used
  if arg.today:
    api.get_today(location)
  elif arg.range:
    api.get_range(location)
  else:
    print("Invalid Option. Choices: [1] -t or --today [2] -r or --range")

if __name__ == '__main__':
  main()
