# Layout.  Handles theming and layout of the main GUI.

import PySimpleGUI as sg

from . import sim_config as cfg
from . import sim_backend

sim = sim_backend.Simulator

####    ####    ####    ####
####    THEME SECTION HERE
COLOR_BG = "#ACABC3"  # light blue-purple
COLOR_DARK = "#242F50"  # navy
COLOR_LIGHT = "#D9FCDC"  # light green

my_theme = {
    "BACKGROUND": COLOR_BG,
    "TEXT": COLOR_DARK,
    "INPUT": COLOR_LIGHT,
    "TEXT_INPUT": COLOR_DARK,
    "SCROLL": COLOR_DARK,
    "BUTTON": (COLOR_LIGHT, COLOR_DARK),  # input, background
    "PROGRESS": (COLOR_DARK, COLOR_LIGHT),
    "BORDER": 1,
    "SLIDER_DEPTH": 0,
    "PROGRESS_DEPTH": 0,
}
sg.theme_add_new("mytheme", my_theme)
sg.theme("mytheme")

####    ####    ####    ####
####    COMMON DICE FRAME STUFFS STARTS HERE
d4_label = sg.Text(
    "D4",
    key="-D4LABEL-",
    size=cfg.BTN_SIZE,
    justification="center",
    pad=((cfg.BTN_MARGIN, cfg.BTN_HPAD), cfg.BTN_VPAD),
)
d6_label = sg.Text(
    "D6",
    key="-D6LABEL-",
    size=cfg.BTN_SIZE,
    justification="center",
    pad=((cfg.BTN_HPAD, cfg.BTN_HPAD), cfg.BTN_VPAD),
)
d8_label = sg.Text(
    "D8",
    key="-D8LABEL-",
    size=cfg.BTN_SIZE,
    justification="center",
    pad=((cfg.BTN_HPAD, cfg.BTN_HPAD), cfg.BTN_VPAD),
)
d10_label = sg.Text(
    "D10",
    key="-D10LABEL-",
    size=cfg.BTN_SIZE,
    justification="center",
    pad=((cfg.BTN_HPAD, cfg.BTN_HPAD), cfg.BTN_VPAD),
)
d12_label = sg.Text(
    "D12",
    key="-D12LABEL-",
    size=cfg.BTN_SIZE,
    justification="center",
    pad=((cfg.BTN_HPAD, cfg.BTN_HPAD), cfg.BTN_VPAD),
)
d20_label = sg.Text(
    "D20",
    key="-D20LABEL-",
    size=cfg.BTN_SIZE,
    justification="center",
    pad=((cfg.BTN_HPAD, cfg.BTN_MARGIN), cfg.BTN_VPAD),
)

d4_plus_btn = sg.Button(
    "+",
    key="-+4-",
    size=cfg.BTN_SIZE,
    pad=((cfg.BTN_MARGIN, cfg.BTN_HPAD), cfg.BTN_VPAD),
)
d6_plus_btn = sg.Button(
    "+", key="-+6-", size=cfg.BTN_SIZE, pad=((cfg.BTN_HPAD, cfg.BTN_HPAD), cfg.BTN_VPAD)
)
d8_plus_btn = sg.Button(
    "+", key="-+8-", size=cfg.BTN_SIZE, pad=((cfg.BTN_HPAD, cfg.BTN_HPAD), cfg.BTN_VPAD)
)
d10_plus_btn = sg.Button(
    "+",
    key="-+10-",
    size=cfg.BTN_SIZE,
    pad=((cfg.BTN_HPAD, cfg.BTN_HPAD), cfg.BTN_VPAD),
)
d12_plus_btn = sg.Button(
    "+",
    key="-+12-",
    size=cfg.BTN_SIZE,
    pad=((cfg.BTN_HPAD, cfg.BTN_HPAD), cfg.BTN_VPAD),
)
d20_plus_btn = sg.Button(
    "+",
    key="-+20-",
    size=cfg.BTN_SIZE,
    pad=((cfg.BTN_HPAD, cfg.BTN_MARGIN), cfg.BTN_VPAD),
)

d4_minus_btn = sg.Button(
    "-",
    key="--4-",
    size=cfg.BTN_SIZE,
    pad=((cfg.BTN_MARGIN, cfg.BTN_HPAD), (cfg.BTN_VPAD, 2 * cfg.BTN_VPAD)),
)
d6_minus_btn = sg.Button(
    "-",
    key="--6-",
    size=cfg.BTN_SIZE,
    pad=((cfg.BTN_HPAD, cfg.BTN_HPAD), (cfg.BTN_VPAD, 2 * cfg.BTN_VPAD)),
)
d8_minus_btn = sg.Button(
    "-",
    key="--8-",
    size=cfg.BTN_SIZE,
    pad=((cfg.BTN_HPAD, cfg.BTN_HPAD), (cfg.BTN_VPAD, 2 * cfg.BTN_VPAD)),
)
d10_minus_btn = sg.Button(
    "-",
    key="--10-",
    size=cfg.BTN_SIZE,
    pad=((cfg.BTN_HPAD, cfg.BTN_HPAD), (cfg.BTN_VPAD, 2 * cfg.BTN_VPAD)),
)
d12_minus_btn = sg.Button(
    "-",
    key="--12-",
    size=cfg.BTN_SIZE,
    pad=((cfg.BTN_HPAD, cfg.BTN_HPAD), (cfg.BTN_VPAD, 2 * cfg.BTN_VPAD)),
)
d20_minus_btn = sg.Button(
    "-",
    key="--20-",
    size=cfg.BTN_SIZE,
    pad=((cfg.BTN_HPAD, cfg.BTN_MARGIN), (cfg.BTN_VPAD, 2 * cfg.BTN_VPAD)),
)

col_d4 = sg.Column(
    [[d4_label], [d4_plus_btn], [d4_minus_btn]], element_justification="center"
)

col_d6 = sg.Column(
    [[d6_label], [d6_plus_btn], [d6_minus_btn]], element_justification="center"
)

col_d8 = sg.Column(
    [[d8_label], [d8_plus_btn], [d8_minus_btn]], element_justification="center"
)

col_d10 = sg.Column(
    [[d10_label], [d10_plus_btn], [d10_minus_btn]], element_justification="center"
)

col_d12 = sg.Column(
    [[d12_label], [d12_plus_btn], [d12_minus_btn]], element_justification="center"
)

col_d20 = sg.Column(
    [[d20_label], [d20_plus_btn], [d20_minus_btn]], element_justification="center"
)

# Frame requires an iterable of iterables, be advised!
dice_frm = sg.Frame(
    "Common Dice", [[col_d4, col_d6, col_d8, col_d10, col_d12, col_d20]]
)

####    COMMON DICE FRAME STUFFS ENDS HERE

####    ####    ####    ####
####    MANUAL INPUT FRAME STUFFS STARTS HERE

man_texthint = sg.Text(
    text="e.g. 1d2+3d4",
    pad=(5, (0, 2)),
    tooltip="For example, to roll four D6s and five D10s,\n" "type 4d6+5d10",
)

man_input = sg.Input(size=17, key="-MAN_INPUT-", enable_events=True)

man_replace = sg.Button(
    "Replace",
    key="-MAN_REPLACE-",
    pad=(5, (3, 5)),
    tooltip="Overwrite current contents of dice pool with above input.",
)

man_append = sg.Button(
    "Append",
    key="-MAN_APPEND-",
    pad=(5, (3, 5)),
    tooltip="Add above input to current dice pool.",
)

manual_layout = [
    [sg.Text("Dice to roll:")],
    [man_texthint],
    [man_input],
    [man_replace, man_append],
]

manual_frm = sg.Frame("Manual Control", manual_layout)

####    MANUAL INPUT FRAME STUFFS ENDS HERE

####    ####    ####    ####
####    DIE POOL FRAME STUFFS STARTS HERE
pool_view = sg.Multiline(
    size=(15, 4),
    key="-POOL_CONTENTS-" + sg.WRITE_ONLY_KEY,
    # Disabled means contents can't be modified in any way
    autoscroll=True,
    disabled=True,
)

pool_clear = sg.Button("Clear Dice Pool", key="-POOL_CLEAR-", pad=(5, (3, 5)))

pool_layout = [
    # Makes this element write-only so that it's not included in values dict
    [pool_view],
    [pool_clear],
]

pool_frm = sg.Frame("Dice Pool", pool_layout)

####    DIE POOL FRAME STUFFS ENDS HERE

####    ####    ####    ####
####    MODE FRAME STUFFS STARTS HERE
mode_sum = sg.Radio(
    text="Sum",
    default=True,
    group_id=1,
    enable_events=True,
    pad=(5, 0),
    circle_color="white",
    key="-MODE_SUM-",
    tooltip="Takes sum of all dice from a given dice roll.",
)

mode_success = sg.Radio(
    text="Successes",
    group_id=1,
    enable_events=True,
    pad=(5, 0),
    circle_color="white",
    key="-MODE_SUCCESS-",
    tooltip="Counts number of successes from a given dice roll.",
)

mode_success_threshold_text = sg.Text(
    "Threshold:",
    pad=((5, 0), 0),
    tooltip="Values greater than equal to this one will be counted as a success.",
)

mode_success_threshold = sg.Spin(
    [1],
    initial_value=1,
    disabled=True,
    key="-MODE_SUCCESS_THRESHOLD-",
    enable_events=True,
    size=2,
)

mode_layout = [
    [mode_sum],
    [mode_success],
    [mode_success_threshold_text],
    [mode_success_threshold],
]

mode_frm = sg.Frame("Mode", mode_layout)

####    MODE FRAME STUFFS ENDS HERE

####    ####    ####    ####
####    REROLL FRAME STUFFS STARTS HERE
reroll_select = sg.Checkbox(
    "Reroll dice",
    pad=(5, (0, 2)),
    key="-REROLL_SELECT-",
    checkbox_color="white",
    enable_events=True,
)

reroll_threshold = sg.Spin(
    list(range(0, 20)),
    0,
    disabled=True,
    key="-REROLL_THRESHOLD-",
    enable_events=True,
    size=2,
    pad=(5, (5, 4)),
)

reroll_layout = [
    [reroll_select],
    [reroll_threshold, sg.Text("and below", pad=((2, 5), (5, 4)))],
]

reroll_frm = sg.Frame("Reroll", reroll_layout)

####    REROLL FRAME STUFFS ENDS HERE

####    ####    ####    ####
####    DROP FRAME STUFFS STARTS HERE
drop_select = sg.Combo(
    ["Do not drop", "Drop lowest", "Drop highest"],
    "Do not drop",
    size=11,
    key="-DROP_SELECT-",
    readonly=True,
    enable_events=True,
)

drop_num = sg.Spin(
    [0],
    initial_value=0,
    key="-DROP_NUM-",
    disabled=True,
    enable_events=True,
    pad=(5, (5, 4)),
    size=2,
)

drop_layout = [[drop_select], [drop_num, sg.Text("Dice", pad=(5, (5, 4)))]]

drop_frm = sg.Frame("Drops", drop_layout)

####    DROP FRAME STUFFS ENDS HERE

####    ####    ####    ####
####    TRIALS FRAME STUFFS STARTS HERE
num_trials_input = sg.Input(
    size=6,
    key="-NUM_TRIALS_INPUT-",
    default_text=sim.num_trials,
    pad=(4, 0),
    enable_events=True,
)

num_trials_commit = sg.Button("Update", pad=((5, 5), 5), key="-NUM_TRIALS_COMMIT-")

num_trials_MoE = sg.Text(
    f"{sim.calculate_MoE()}%",
    pad=((0, 5), 5),
    size=5,
    justification="right",
    key="-NUM_TRIALS_MOE-",
    tooltip="Estimated margin of error, in percentage points, of each data bar.",
)

num_trials_CI_text = sg.Text(
    "CI (%):",
    pad=((4, 0), 5),
    tooltip="Confidence interval.  Roughly speaking, an n % confidence interval means\n"
    "the depicted data bars will be within the margin of error percentage points\n"
    "of the true probability, n % of the time.",
)

num_trials_CI = sg.Combo(
    [key for key in cfg.ZSTAR_VALS],
    enable_events=True,
    default_value=sim.CI_level,
    size=2,
    key="-NUM_TRIALS_CI-",
    pad=((5, 5), 5),
)

num_trials_layout = [
    [sg.Text("Number of trials:", pad=(5, 0)), num_trials_input, num_trials_commit],
    [
        sg.Text("Est. MoE: +/-", pad=((5, 0), 5)),
        num_trials_MoE,
        num_trials_CI_text,
        num_trials_CI,
    ],
]

trials_frm = sg.Frame("Trials", num_trials_layout)

####    TRIALS FRAME STUFFS ENDS HERE

####    ####    ####    ####
####    CREDITS FRAME STUFFS STARTS HERE
credits_layout = [
    [sg.Text("Made with <3 by Aerie")],
    [sg.Text(f"v {cfg.VERSION}")],
]

credits_frm = sg.Frame("About", credits_layout)

####    CREDITS FRAME STUFFS ENDS HERE

####    ####    ####    ####
####    (LEFT) SUBCOLUMNS STUFFS STARTS HERE
col_L1 = sg.Column(
    [[reroll_frm, drop_frm], [trials_frm], [credits_frm]], element_justification="left"
)

btn_engage = sg.Button(" Run Simulation ", size=12, key="-ENGAGE-", pad=(5, (10, 2)))

btn_save_output = sg.Button(
    " Save Output... ", size=12, key="-SAVE_OUTPUT-", pad=(5, (5, 5))
)

btn_credits = sg.Button(" Credits ", size=12, key="-CREDITS-", pad=(5, (27, 5)))

col_L2 = sg.Column(
    [[mode_frm], [btn_engage], [btn_save_output], [btn_credits]],
    element_justification="center",
)

####    (LEFT) SUBCOLUMNS STUFFS ENDS HERE

####    ####    ####    ####
####    LEFT AND RIGHT COLUMN STUFFS STARTS HERE
col_left = [
    [dice_frm],
    [manual_frm, pool_frm],
    sg.vtop([col_L1, col_L2]),
]

col_right = [
    [
        sg.Canvas(
            size=(cfg.PLT_WIDTH * cfg.PLT_DPI, cfg.PLT_HEIGHT * cfg.PLT_DPI),
            key="-CANVAS-",
            pad=(10, 10),
        )
    ]
]

####    LEFT AND RIGHT COLUMN STUFFS ENDS HERE

####    ####    ####    ####
####    FULL LAYOUT
layout = [
    [
        sg.Column(col_left, vertical_alignment="top", element_justification="center"),
        sg.VerticalSeparator(),
        sg.Column(col_right),
    ]
]
