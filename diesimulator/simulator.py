# Simulator frontend.  Activates PSG and runs main program.

import PySimpleGUI as sg

import diesimulator.sim_config as cfg
import diesimulator.sim_backend
import diesimulator.sim_layout as slay
import diesimulator.sim_gui_element_ops as sops
import diesimulator.sim_icon as sicon

sim = diesimulator.sim_backend.Simulator


def create_window():
    return sg.Window(
        f"Aerie Dice Roll Simulator v {cfg.VERSION}",
        layout=slay.layout,
        icon=sicon.icon,
        finalize=True,
        use_default_focus=False,
    )


window = create_window()

while True:
    # In PSG, events are keys; values is a returned dict corresponding to
    #  element inputs or changes.
    event, values = window.read()

    # Quitting events
    if event in (sg.WIN_CLOSED, None):
        break

    # Button events for inc/decrementing common dice
    if event[1] in ("+", "-"):
        # String slicing to extract operation and die from event
        sim.modify_dice(int(event[2:-1]), event[1])

    # Handle events related to manual input
    #  slices the string to pass "sub-event" into man_ops()
    if event[1:4] == "MAN":
        sops.man_ops(window, event[5:-1], values)

    # Handle clicking of the "Clear die pool" button
    if event == "-POOL_CLEAR-":
        sim.clear_die_pool()

    # Handle events dealing with the mode selection frame
    #  slices the string to pass "sub-event" into mode_ops()
    if event[1:5] == "MODE":
        sops.mode_ops(window, event[6:-1])

    # Handle events dealing with the drop selection frame,
    #  passes in current state of dropdown in values dictionary
    if event[1:5] == "DROP":
        sops.drop_ops(window, values["-DROP_SELECT-"])

    # Handle events dealing with the reroll selection checkbox,
    #  passing in enabled state of checkbox as bool
    if event == "-REROLL_SELECT-":
        sops.reroll_select_ops(window, window["-REROLL_SELECT-"].get())

    # Handle events dealing with the trials frame
    #  slices the string to pass "sub-event" into num_trials_ops()
    if event[1:11] == "NUM_TRIALS":
        sops.num_trials_ops(window, event[12:-1], values)

    # Update dice pool text
    sops.pool_update(window)

    # Element updates that must be checked/performed for *any* event
    # If input errors detected, flag will equal 1; 0 else
    # Input error flag checked immediately below if ENGAGE event is triggered
    input_error_flag = sops.element_update(window, values)

    # Runs simulation sequence (simulate, sanitize, plot, draw)
    if event == "-ENGAGE-":
        sops.engage_ops(window, input_error_flag)

    # Saves figure to file
    if event == "-SAVE_OUTPUT-":
        sops.save_output_ops()

    # Displays credits
    if event == "-CREDITS-":
        sops.credits_ops()

    window.refresh()

window.close()
