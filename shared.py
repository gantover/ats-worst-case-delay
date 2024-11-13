import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

MAX_PRIORITY = 7 # TODO : read that value in the file directly
RATE = 1e9 / 8 # rate of transmission in the links
OVERHEAD = 42 # bytes
