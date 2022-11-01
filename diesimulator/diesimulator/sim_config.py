# Configuration.  Config and default settings.

VERSION = "1.0.0"
LAST_UPDATED = "10/31/2022"

####    ####    ####    ####
####    VALUES FOR SIMULATOR STUFFS STARTS HERE

# Dict containing critical z* values for selected confidence intervals
ZSTAR_VALS = {70: 1.036, 80: 1.281, 90: 1.645, 95: 1.96, 97: 2.17, 99: 2.576}

# If a data value is at least this number of times smaller than
#  the largest data value, remove it from the plot
CUTOFF_SENSITIVITY = 120

# Number of decimal places to round results to truncate floating-point
#  inaccuracies in representation
ROUNDING_PREC = 6

####    VALUES FOR SIMULATOR STUFFS ENDS HERE

####    ####    ####    ####
####    VALUES FOR PLOT STUFFS STARTS HERE

# Plot dimensions in inches, DPI in pixels
PLT_WIDTH = 9
PLT_HEIGHT = 5
PLT_DPI = 100

# Default label spacing for the actual historgram bars
#  1 means label each bar, 2 means skip every other one, etc.
#  this value may get overwritten if there are too many bars on plot
#  (see label spacing threshold below)
PLT_LBL_SPACING = 1

# Number of bars on graph before alternate label spacing rules kick in
#  if above this threshold, number of labels is approximately equal to
#  number of bars divided by this parameter
PLT_LBL_SPACING_THRESHOLD = 28

# Number of labeled x-axis labels along bottom of graph (approximate)
PLT_X_AX_LABELS_POP = 16

# Value above which x-axis labels become written in scientific notation
PLT_X_AX_SCI_THRESHOLD = 999

# Number of major y-gridlines (excluding x-axis) to be displayed
#  graph will adjust vertical scaling to conform to this value
#  best to pick a smaller value with relatively abundant factors;
#  4 and 6 work well as a default.
PLT_Y_GRIDLINES = 4

####    VALUES FOR PLOT STUFFS ENDS HERE

####    ####    ####    ####
####    VALUES FOR LAYOUT STUFFS STARTS HERE

# Button size for the D(n) +/- buttons
BTN_SIZE = 3
# Horizontal and vertical padding for the D(n) +/- buttons, in pixels
BTN_HPAD = 5
BTN_VPAD = 3
# For D(n) +/- buttons, distance btwn edge buttons and frame, in pixels
BTN_MARGIN = 15

####    VALUES FOR LAYOUT STUFFS ENDS HERE
