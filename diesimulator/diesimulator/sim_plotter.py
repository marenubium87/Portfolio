# Plotter.  Handles everything graph related - labels, axes...
#  also generates plot figure.

import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as plttick
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from . import sim_config as cfg
from . import sim_backend

matplotlib.use("TkAgg")

sim = sim_backend.Simulator


class Plotter:
    # Sorted x and y lists to generate histogram
    x_sorted = []
    y_sorted = []

    # Plot figure object
    fig = None

    # Interface for TKinter fig adaptor
    fig_agg = None

    # Default label spacing for historgram bars
    #  see config for more info
    plt_lbl_spacing = cfg.PLT_LBL_SPACING

    # Thresholds for modes when calculating y-dimension (top of graph)
    y_dim_mode_threshold = [33, 9, 0.7]
    # Minimum proportion the top of graph must be above highest data bar
    min_h = 1.19

    # Step size for cumulative probability distribution function thresholds
    #  for example, step size of 25 would result in cumulative probability
    #  values reported at 25, 50, and 75 percent
    plt_cdf_prob_step = 25

    # Statistical variables - mean and standard deviation
    xbar = 0
    sx = 0

    # Labels
    lbl_data = []
    lbl_quartiles = []

    @classmethod
    def generate_sorted_lists(cls):
        """
        Splits Simulator's freq dictionary into two lists for matplotlib,
        sorted by outcome of roll:
        - x: outcome
        - y: frequency (in percent of total trials)
        """
        cls.x_sorted.clear()
        cls.y_sorted.clear()

        for outcome in sorted(sim.freq.keys()):
            cls.x_sorted.append(outcome)
            cls.y_sorted.append(sim.freq[outcome])

    @classmethod
    def calc_xbar(cls, freq):
        """
        Calculates x-bar for the distribution using frequency dict
        Uses standard Σ x * p(x) formula; rounds to places defined in cfg
        Must be run before calc_sx()
        """
        weighted_sum = 0
        for outcome in freq.keys():
            weighted_sum += outcome * freq[outcome] / 100
        cls.xbar = round(weighted_sum, cfg.ROUNDING_PREC)

    @classmethod
    def calc_sx(cls, freq, xbar):
        """
        Calculates the standard deviation of the distribution using frequency
        dict and rounds to places defined in cfg
        Uses variance shortcut equation; specifically:
        s^2 = Σ [x^2 * p(x)] - x-bar^2
        Must call after calc_xbar(); depends on correct value of x-bar in class
        """
        weighted_sq_sum = 0
        for outcome in freq.keys():
            weighted_sq_sum += (outcome**2) * freq[outcome] / 100

        weighted_sq_sum -= xbar**2
        cls.sx = round(math.sqrt(weighted_sq_sum), cfg.ROUNDING_PREC)

    @classmethod
    def calc_quartiles(cls, freq):
        """
        Generates a list of outcome values that correspond to the
        location of the three quartiles (Q1, M, Q3) of the distribution
        """

        # List that will store cumulative distribution fcn, that is,
        #  each p(x <= i) for i in [min outcome, max outcome]
        #  as tuples in form (outcome, probability)
        cdf = [(-1, 0)]

        # Generate CDF
        for outcome in sorted(freq.keys()):
            cdf.append((outcome, round(freq[outcome] + cdf[-1][1], cfg.ROUNDING_PREC)))

        # Step size to generate CDF thresholds; for quartiles, use 25
        #  i.e. [25, 50, 75]
        step = 25
        prob_threshold_current = step
        # The outcomes that correspond to CDF values exceeding each step
        #  as described above
        new_quartiles = []

        # Build quartiles list
        i = 0
        while prob_threshold_current < 100 and i < len(cdf):
            if cdf[i][1] > prob_threshold_current:
                new_quartiles.append(cdf[i][0])
                prob_threshold_current += step
            i += 1

        cls.quartiles = new_quartiles

    @classmethod
    def generate_x_axis(cls, ax):
        """
        Sets up labels and settings for x-axis, using the
        matplotlib ax axis object and the calculated label spacing
        """
        # Default number of x-labels
        num_x_labels = cfg.PLT_X_AX_LABELS_POP

        # If largest outcome value is greater than scientific threshold,
        #  set x-labels to scientific notation, and
        #  prune number of labels by additional factor of two for spacing
        if cls.x_sorted[-1] > cfg.PLT_X_AX_SCI_THRESHOLD:
            num_x_labels = int(num_x_labels / 2)
            ax.xaxis.set_major_formatter(FormatStrFormatter("%.1e"))

        # Creates x-index from smallest to largest values, and modify
        #  label spacing as necessary for "crowded" x-axes
        ind_x = np.arange(
            cls.x_sorted[0],
            cls.x_sorted[-1] + 1,
            max(int((cls.x_sorted[-1] - cls.x_sorted[0]) / num_x_labels), 1),
        )

        ax.set_xlabel("Outcome")
        ax.set_xticks(ind_x, ind_x)

    @classmethod
    def calc_y_dim(cls):
        """
        Calculates and returns an appropriate y_dim, y-dimension of the graph
        y_dim is *NOT* equal to the highest bar on the graph; needs to be
        higher to leave space at top.
        y_dim_min_threshold - list of cutoffs for calculation modes of y_dim
        min_h - minimum proportion for top of graph above highest data bar
        Necessary for: generate_y_axis()
        """
        # y_dimension of the graph, which is equivalent to the highest value
        #  displayed on the graph window itself (henceforth colloquially
        #  'top of graph'), since bottom value necessarily must be zero
        y_dim = 0

        # Largest data value
        y_data_max = max(sim.freq.values())

        # Mode 1 - Peak of data above highest threshold
        # Possible top of graph values 40 - 120, count by 20
        if y_data_max >= cls.y_dim_mode_threshold[0]:
            y_dim = int(math.ceil(y_data_max * cls.min_h / 10))
            if y_dim % 2 == 1:
                y_dim += 1
            y_dim *= 10

        # Mode 2 - Peak of data < highest; and >= second highest threshold
        #  Top of graph must now be divisible by the gridline number value,
        #  for neat (integer) values on y-axis
        elif y_data_max >= cls.y_dim_mode_threshold[1]:
            y_dim = (
                math.ceil(y_data_max * cls.min_h / cfg.PLT_Y_GRIDLINES)
                * cfg.PLT_Y_GRIDLINES
            )

        # Mode 3 - Peak of data < second highest; and >= lower threshold
        #  Peaks now too small to insist on integer divisibility for gridlines
        #  but force top of graph to still be integer value
        elif y_data_max > cls.y_dim_mode_threshold[2]:
            y_dim = math.ceil(y_data_max * cls.min_h)

        # Mode 4 - Peak of data < lower threshold
        #  Calculate a reasonable value for top of graph, no other restrictions
        else:
            y_dim = y_data_max * cls.min_h

        return y_dim

    @classmethod
    def generate_y_axis(cls, ax):
        """
        Sets up labels and settings for y-axis, using matplotlib axis object
        Requires: calc_y_dim()
        """
        y_dim = cls.calc_y_dim()
        # Y-axis dimension bounds
        ax.set_ylim([0, y_dim])

        # Draw number of gridlines as defined by config file at equally spaced
        #  intervals; minor gridlines at half the distance between majors
        ax.yaxis.set_major_locator(MultipleLocator(y_dim / cfg.PLT_Y_GRIDLINES))
        ax.yaxis.set_minor_locator(MultipleLocator(y_dim / cfg.PLT_Y_GRIDLINES / 2))

        # In this context color is a string decimal btwn 0 (black) and 1 (white)
        ax.grid(axis="y", which="major", linewidth=0.7, color="0.7", linestyle="--")
        ax.grid(axis="y", which="minor", linewidth=0.5, color="0.3", linestyle=":")

        # Make y-axis labels contain decimals if values are small
        y_round_prec = 0
        if max(sim.freq.values()) <= cls.y_dim_mode_threshold[1]:
            y_round_prec += 2

        # Sets up y-axis formatting for percents, but without percent symbols
        ax.yaxis.set_major_formatter(
            plttick.PercentFormatter(decimals=y_round_prec, symbol="")
        )

        # Draws gridlines underneath data bars
        ax.set_axisbelow(True)
        ax.set_ylabel("Probability (%)")

    @classmethod
    def calc_lbl_spacing(cls):
        """
        Determines whether to use alternate label spacing rules, and
        determines an appropriate label spacing
        """
        # Resets plot spacing; necessary for running a simulation not requiring
        #  alternative label spacing, after running a simulation that did
        cls.plt_lbl_spacing = 1

        # Alternative label spacing threshold calculation, if applicable.
        if max(sim.freq.keys()) - min(sim.freq.keys()) > cfg.PLT_LBL_SPACING_THRESHOLD:
            cls.plt_lbl_spacing = math.ceil(
                (max(sim.freq.keys()) - min(sim.freq.keys()))
                / cfg.PLT_LBL_SPACING_THRESHOLD
            )

    @classmethod
    def generate_lbl_list(cls):
        """
        Labels for data bars, based on plotter label spacing attribute
        """
        cls.lbl_data = [str(round(y, 1)) for y in cls.y_sorted]

        # Eliminates values from being labeled according to label spacing param
        for i in range(len(cls.lbl_data)):
            if i % cls.plt_lbl_spacing != 0:
                cls.lbl_data[i] = ""

    @classmethod
    def generate_quartile_list(cls):
        """
        Generates a list for the quartile labels
        """
        quartile_names = ["Q1", "M", "Q3"]
        # Merges quartile values and names into dict
        quartile_dict = {
            cls.quartiles[i]: quartile_names[i] for i in range(len(cls.quartiles))
        }

        # Clear labels from previous run
        cls.lbl_quartiles = []
        for i, outcome in enumerate(cls.x_sorted):
            if outcome in quartile_dict:
                # Adds quartile labels in correct location
                cls.lbl_quartiles.append(quartile_dict[outcome])
                # Also clears the surrounding neighborhood
                #  [-(spacing - 1), (spacing - 1)] around the quartile marker
                #  from data labels, so that figures don't overlap
                for j in range(i - cls.plt_lbl_spacing + 1, i + cls.plt_lbl_spacing):
                    cls.lbl_data[j] = ""
            else:
                cls.lbl_quartiles.append("")

    @classmethod
    def generate_lbls_highlights(cls, graph, ax, color_dark, color_light):
        """
        Wrapper handling labels and highlighting tasks on the bar graph object
        color_dark is for quartile bar edges and labels
        color_light is for quartile bar faces
        """
        # Update label spacing first, then generate label lists
        cls.calc_lbl_spacing()
        cls.generate_lbl_list()
        cls.generate_quartile_list()

        # Place data labels
        # Padding is distance above the relevant bar to place labels
        ax.bar_label(graph, fmt="%.1f", labels=cls.lbl_data, padding=8)

        # Place quartile labels
        ax.bar_label(
            graph,
            labels=cls.lbl_quartiles,
            padding=8,
            color=color_dark,
            fontweight="heavy",
        )

        # Highlight quartile bars
        for i, label in enumerate(cls.lbl_quartiles):
            if label != "":
                graph[i].set(color=color_light, edgecolor=color_dark)

    @classmethod
    def generate_annotations(cls, ax, color_dark, color_light):
        """
        Creates a vertical line marker in color_light 
        and annotates values for xbar and sd in color_dark
        """
        # Draw vertical line for x-bar location
        plt.vlines(
            x=cls.xbar,
            ymin=ax.get_ylim()[1] * 0.85,
            ymax=ax.get_ylim()[1] * 0.97,
            linewidths=1.7,
            color=color_light
        )
        # Note value of x-bar and std dev nearby
        plt.annotate(
            "x-bar = \n s.d. = ",
            xy=(cls.xbar, ax.get_ylim()[1] * 0.94),
            xytext=(
                cls.xbar + (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.08,
                ax.get_ylim()[1] * 0.91,
            ),
            ha="right",
            color=color_dark
        )
        plt.annotate(
            f"{round(cls.xbar, 1)}\n" f"{round(cls.sx, 1)}",
            xy=(cls.xbar, ax.get_ylim()[1] * 0.94),
            # Calculates an offset from the vertical line for text placement
            xytext=(
                cls.xbar + (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.13,
                ax.get_ylim()[1] * 0.91,
            ),
            ha="right",
            color=color_dark
        )

    @staticmethod
    def generate_title():
        """
        Reads parameters from Simulator to dynamically generate title string
        """
        mode_str = sim.mode

        dice_str = sim.generate_dice_str_from_pool()

        success_threshold_str = ""
        # Doesn't make sense to print out success threshold if it's equal to 1
        #  (those are auto-successes)
        if sim.success_threshold > 1:
            success_threshold_str = f" (>= {sim.success_threshold})"

        reroll_str = ""
        # Doesn't make sense to print out reroll threshold is it's equal to 0
        #  (there will be no rerolls)
        if sim.reroll_threshold > 0:
            reroll_str = f", Reroll <= {sim.reroll_threshold}"

        drop_str = ""
        # Doesn't make sense to print out number of drops if it's equal to 0
        #  (since we aren't dropping anything)
        if sim.num_drops > 0:
            drop_str = f", {sim.mode_drop} {sim.num_drops}"

        trials_str = f", {sim.num_trials} Trials"

        plt.title(
            f"{mode_str}"
            f"{success_threshold_str} of {dice_str}{reroll_str}"
            f"{drop_str}{trials_str}"
        )

    @classmethod
    def generate_plot(cls):
        """
        Sets up matplotlib plot from freq dictionary; returns figure of plot
        Requires:  all class functions above.
        """
        # Do not plot if no usable data
        if not sim.freq:
            return
        # Closes previous figures, if any
        plt.close("all")

        # Create sorted lists for matplotlib from sim's freq dictionary
        cls.generate_sorted_lists()

        # Calculate statistical parameters
        cls.calc_xbar(sim.freq)
        cls.calc_sx(sim.freq, cls.xbar)
        cls.calc_quartiles(sim.freq)

        # Initialize figure and axes
        fig, ax = plt.subplots()

        # Sets figure width and height in inches
        fig.set_size_inches(cfg.PLT_WIDTH, cfg.PLT_HEIGHT)

        # Graph colors here
        color_bar_dark = "#324A99"  # dark blue
        color_bar_light = "#ADC7FF"  # light blue
        color_quartile_dark = "#104722"  # dark green
        color_quartile_light = "#86F7AA"  # lighter green
        color_annotate_dark = "#3B1D8F"  # dark violet
        color_annotate_light = "#D6C7FF"  # lavender

        # Generate bar graph object with data; draw bars
        bar_graph = ax.bar(
            cls.x_sorted,
            cls.y_sorted,
            color=color_bar_light,
            edgecolor=color_bar_dark,
            linewidth=1.4,
        )

        # Generate and format x- and y- axes
        cls.generate_x_axis(ax)
        cls.generate_y_axis(ax)

        # Labels, annotations, and title
        cls.generate_lbls_highlights(bar_graph, ax, color_quartile_dark, color_quartile_light)
        cls.generate_annotations(ax, color_annotate_dark, color_annotate_light)
        cls.generate_title()

        plt.tight_layout()
        # Returns current figure
        return plt.gcf()


# Matplotlib helper code from PySimpleGUI documentation
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg
