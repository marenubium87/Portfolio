# Element operations.  Contains functions for element event activations on GUI.

import PySimpleGUI as sg

from . import sim_backend
from . import sim_plotter as splot

sim = sim_backend.Simulator
plotter = splot.Plotter


def parse_input(input_str):
    """
    Parses user input str from manual input field and returns a dice diction
    in the format (type: number)
    Necessary for: man_ops()
    """
    temp_dice = {}
    # Split into groups based on the + character
    die_groups = input_str.split("+")
    for group in die_groups:
        temp = group.split("d")
        # Should catch all invalid entries for dice in _d_ format
        if len(temp) != 2:
            return {}
        if not temp[0].isdigit() or not temp[1].isdigit():
            return {}
        if int(temp[0]) < 1 or int(temp[1]) < 1:
            return {}
        # Otherwise, values are valid; convert to ints and
        temp[0] = int(temp[0])
        temp[1] = int(temp[1])
        # Append or add entries to temp_dice dictionary
        #  append will catch degenerate input, such as 3d6+2d6 (=5d6)
        if temp[1] in temp_dice:
            temp_dice[temp[1]] = temp_dice[temp[1]] + temp[0]
        else:
            temp_dice[temp[1]] = temp[0]
    return temp_dice


def element_update_successes(window, values):
    """
    Update function for simulator mode and success threshold elements
    sub-function of element_update()
    Returns 0 if no success threshold is in valid state, 1 otherwise
    """
    # Redefinition for convenience
    mst_window = window["-MODE_SUCCESS_THRESHOLD-"]
    mst_str = values["-MODE_SUCCESS_THRESHOLD-"]

    # If value of the success threshold is not an int...
    if mst_str and not isinstance(mst_str, int):
        # Can it be read as an int greater than zero?
        if mst_str.isdigit() and int(mst_str) > 0:
            pass
        else:
            # If not, input is malformed; reset to valid state and return error
            mst_window.update(value=1)
            return 1

    if sim.dice:
        biggest_die = 0
        mst_window.update(disabled=False)

        # In other words, this is the largest value that can occur on any single
        #  die in the pool
        biggest_die = max(sim.dice)
        # Range starts at 1 because it makes no sense to ever have
        #  a success threshold of 0
        mst_window.update(values=list(range(1, biggest_die + 1)))
        # Updates selection for situation where a larger faced die is removed
        #  this also triggers if user inputs value greater than largest die
        if int(mst_window.get()) > biggest_die:
            mst_window.update(value=biggest_die)
    else:
        # Disables and resets spinner if dice pool is empty
        mst_window.update(value=1, values=[1], disabled=True)

    # Update simulator success threshold from value in spinner
    sim.success_threshold = int(mst_window.get())
    return 0


def element_update_drops(window, values):
    """
    Update function for operations involving dropping dice
    sub-function of element_update()
    """
    # Prevents an annoying error when dice pool is empty,
    #  causing window to report a value of -1
    total_dice = 1
    if sim.dice:
        total_dice = sim.get_total_dice()

    # Redefinition for convenience
    dn_window = window["-DROP_NUM-"]
    dn_str = values["-DROP_NUM-"]

    # If value of the number of drops is not an int...
    if dn_str and not isinstance(dn_str, int):
        # Can it be read as an int greater than zero?
        if dn_str.isdigit() and int(dn_str) >= 0:
            pass
        else:
            # If not, input is malformed; reset to valid state and return error
            dn_window.update(value=0)
            return 1

    # NOT an off-by-one error here; it doesn't make sense to drop all the dice
    #  so the correct interval is [0, total_dice)
    dn_window.update(values=list(range(0, total_dice)))

    # Updates selection for situation when dice are removed
    if int(dn_window.get()) >= total_dice:
        dn_window.update(value=total_dice - 1)

    # Update simulator number of drops from value in spinner
    sim.num_drops = int(dn_window.get())
    return 0


def element_update_reroll(window, values):
    """
    Update function for operations involving rerolling dice
    sub-function of element_update()
    """
    # Prevents an annoying error when dice pool is empty,
    #  causing window to report a value of -1
    smallest_die = 1
    if sim.dice:
        smallest_die = min(sim.dice)
    # Redefinition for convenience
    rt_window = window["-REROLL_THRESHOLD-"]
    rt_str = values["-REROLL_THRESHOLD-"]

    # If value of the reroll threshold is not an int...
    if rt_str and not isinstance(rt_str, int):
        # Can it be read as an int greater than zero?
        if rt_str.isdigit() and int(rt_str) >= 0:
            pass
        else:
            # If not, input is malformed; reset to valid state and return error
            rt_window.update(value=0)
            return 1

    # NOT an off by one error - we want the interval to be [0, smallest_die)
    #  (in other words, not inclusive), since if we have to reroll the largest
    #  value on the smallest die then we'll be rerolling forever
    rt_window.update(values=list(range(0, smallest_die)))

    # Updates selection for situation where a larger faced die is removed
    if int(rt_window.get()) >= smallest_die:
        rt_window.update(value=smallest_die - 1)

    # Update simulator reroll threshold from value in spinner
    sim.reroll_threshold = int(rt_window.get())
    return 0


def element_update(window, values):
    """
    Wrapper that runs all potential items that must be checked and possibly
    updated for *any* action that is taken in the program
    If any errors are detected in input for any of the subfunctions, will
    abort update for remainder and return 1; if no errors are detected return 0
    Requires: all sub-functions of the form element_update_(...) above
    """
    errors_detected = 0
    if sim.mode == "Successes" and not errors_detected:
        errors_detected = element_update_successes(window, values)

    if sim.mode_drop != "Do not drop" and not errors_detected:
        errors_detected = element_update_drops(window, values)

    # This if statement checks whether the "reroll select" checkbox is checked
    if window["-REROLL_SELECT-"].get() and not errors_detected:
        errors_detected = element_update_reroll(window, values)

    return errors_detected


def pool_update(window):
    """
    Update function for dice pool multiline text element; should be run
    once per cycle to update text in dice pool
    """
    # Write-only key prevents contents from being unnecessarily stored
    #  in PSG's values dictionary
    # Redefinition for convenience
    pool_window = window["-POOL_CONTENTS-" + sg.WRITE_ONLY_KEY]
    # Clear and rebuild string

    pool_window.update("")
    if sim.dice:
        pool_str = ""
        for die_type, die_num in sim.dice.items():
            pool_str += f"{die_num} D{die_type}\n"
        # Clears up a newline at the end of output
        pool_window.update(pool_str[:-1])


def man_ops(window, event, values):
    """
    Operations that must be performed for interaction with elements in the
    manual operation frame.  Pass in "sub-event" for any event starting
    with "MAN" and performs appropriate operations
    Requires: parse_input()
    """
    # Redefinitions for convenience
    mi_str = values["-MAN_INPUT-"]
    mi_window = window["-MAN_INPUT-"]

    if event == "INPUT":
        # Input validation.  Should delete any character that's not
        #  a numeral, d, +
        if mi_str and mi_str[-1] not in ("0123456789d+"):
            mi_window.update(mi_str[:-1])

    if event in ["REPLACE", "APPEND"]:
        # Generates new dice dictionary from user input
        new_dice_dict = parse_input(mi_window.get())
        # If input is malformed, dice dict should be empty
        if not new_dice_dict:
            sg.popup(
                "Unable to parse your dice string; please check your input.",
                title="Error Parsing Input",
            )
        else:
            mi_window.update(value="")
            # Replaces or appends to current dice dictionary depending on mode
            if event == "REPLACE":
                sim.clear_die_pool()
            for die_type, die_num in new_dice_dict.items():
                sim.modify_dice(die_type, "+", die_num)


def mode_ops(window, event):
    """
    Operations that must be performed for interaction with elements in the
    mode selection frame.  Pass in "sub-event" for any event starting
    with "MODE" and performs appropriate operations
    """
    # Note: success threshold is updated in universal element update,
    #  and not here
    if event in ["SUM", "SUCCESS"]:
        # Redefinition for convenience
        mst_window = window["-MODE_SUCCESS_THRESHOLD-"]
        if event == "SUM":
            sim.mode = "Sum"
            mst_window.update(disabled=True, value=1)
            sim.success_threshold = 1
        if event == "SUCCESS":
            sim.mode = "Successes"
            mst_window.update(disabled=False, value=1)


def drop_ops(window, mode):
    """
    Operations that must be performed for interaction with elements in the
    drop dice frame.  Pass in mode from the drop mode combobox to perform
    actions accordingly
    Mode has possible values {'Do not drop', 'Drop lowest', 'Drop highest'}
    """
    # Note: Number of drops is updated in universal element update,
    #  and not here
    sim.mode_drop = mode

    # Redefinition for convenience
    dn_window = window["-DROP_NUM-"]
    if mode == "Do not drop":
        dn_window.update(disabled=True, value=0)
    else:
        dn_window.update(disabled=False)


def reroll_select_ops(window, enabled):
    """
    Operations that must be performed for interaction with elements in the
    reroll selection frame.  Uses bool current enabled state of reroll checkbox
    """
    # Note: Success threshold is updated in universal element update,
    #  and not here
    # Redefinition for convenience
    rt_window = window["-REROLL_THRESHOLD-"]

    if enabled:
        rt_window.update(disabled=False)
    else:
        rt_window.update(disabled=True, value=0)
        sim.num_drops = 0


def num_trials_ops(window, event, values):
    """
    Operations that must be performed for interaction with elements in the
    number of trials frame and margin of error frame.  Pass in "sub-event" for
    any event starting with "NUM_TRIALS" and performs appropriate operations
    """
    # Redefinition for convenience
    nt_str = values["-NUM_TRIALS_INPUT-"]
    nt_window = window["-NUM_TRIALS_INPUT-"]

    if event == "INPUT":
        # Input validation - should delete any character that's not
        #  a numeral
        if nt_str and nt_str[-1] not in ("0123456789"):
            nt_window.update(nt_str[:-1])

    if event == "COMMIT":
        # Makes certain that input is readable as a numeral
        #  clears any input that is malformed and warns user
        if nt_str.isdigit() and int(nt_str) > 0:
            sim.num_trials = int(nt_str)
            window["-NUM_TRIALS_MOE-"].update(value=f"{sim.calculate_MoE()}%")
        else:
            sg.popup(
                "Please enter a valid (integer, positive) number of trials.",
                title="Input Error",
            )
            sim.num_trials = 0
        nt_window.update(value=sim.num_trials)

    if event == "CI":
        sim.CI_level = int(window["-NUM_TRIALS_CI-"].get())


def engage_ops(window, input_error_flag):
    """
    Operations that must be performed when the user hits the
    'Run Simulation' button.  Runs simulation and draws graph
    assuming no errors in input.
    """
    # Verify no errors in input from earlier
    if input_error_flag:
        sg.popup(
            (
                "One or more input parameters is not\na valid value"
                " and has been reset.\n\n"
                "Please check your inputs and try again."
            ),
            title="Input Error",
        )
    elif not sim.dice:
        sg.popup("No dice in pool; simulation aborted.", title="Dice Pool Error")
    elif sim.num_trials < 1:
        sg.popup(
            "Non-positive number of trials; simulation aborted.",
            title="Number of Trials Error",
        )
    else:
        # clear previous canvas
        if plotter.fig_agg is not None:
            plotter.fig_agg.get_tk_widget().forget()

        sim.perform_sim()
        window.refresh()
        sim.sanitize_outcomes()
        plotter.fig = plotter.generate_plot()

        plotter.fig_agg = splot.draw_figure(window["-CANVAS-"].TKCanvas, plotter.fig)


def save_output_ops():
    """
    Operations that must be performed when the user hits the
    'Save Output' button
    """
    if plotter.fig is not None:
        file_path = sg.popup_get_file(
            "Choose path to save figure (PNG):",
            save_as=True,
            title="Save Figure",
            default_extension=".png",
            # Value is a tuple of a tuple, hence the double parens
            #  and the single comma
            file_types=(("Image File (.png)", "*.png"),),
        )
        if file_path is not None:
            splot.plt.savefig(f"{file_path}")
            sg.popup(f"Output saved as {file_path}.", title="Save Successful")


def credits_ops():
    """
    Operations peformed when the user hits the 'Credits' button
    """
    sg.popup(
        "Credits:\n\n"
        "Developer:  Birb (Aerie)\n"
        "Guidance:   Kitty (Mrow)\n"
        "Testing:    Wickerbeast (Lyra)\n"
        "End-user:   You!  Thank you <3",
        font="Consolas",
        title="Credits",
    )
