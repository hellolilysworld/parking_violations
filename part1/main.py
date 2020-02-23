import os
import sys
import json
import pprint
import pandas as pd
import numpy as np
import argparse
from functools import reduce

from src.bigdata1.api import get_results, add_record

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--page_size", type=int)
    parser.add_argument("--num_pages", default=4, type=int)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    get_results(args.page_size, args.num_pages, args.output)
    



    
