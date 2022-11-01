# Simulator backend.  Handles simulating die rolls, and preparing, sanitizing,
#  and aggregating results for use by plotter.

import math
import random as rand

from . import sim_config as cfg


class Simulator:
    # Dictionary where keys are types of dice and vals are number of that die
    #  e.g. 6:2 would mean 2d6
    dice = {}

    # Operation mode
    #  available modes {'Sum', 'Successes'}
    mode = "Sum"

    # Die roll must be >= this number to be counted as a success, min 1
    success_threshold = 1

    # Dice drop mode
    #  available modes {'Do not drop', 'Drop lowest', 'Drop highest'}
    mode_drop = "Do not drop"
    # Number of dice to drop
    num_drops = 0
    # Reroll all dice equal to or below this number
    reroll_threshold = 0

    # Simulation trials to run
    num_trials = 60000

    # The confidence level for MoE calculations
    #  must be one of the confidence interval values in cfg file!
    CI_level = 90

    # Dictionary storing outcomes as keys and frequencies as values
    #  for any given simulation run
    freq = {}

    @classmethod
    def modify_dice(cls, die_type, operation, n=1):
        """
        Modifies Simulator's dice dictionary entry of die_type
        by n dice and by the relevant operation string.
        If die_type doesn't exist in dict, it will be created.

        Acceptable values for operation are as follows:
        +:  adds one die of the type to the die pool
        -:  subtracts one die of the type from the die pool
        =:  sets the number of dice of type to n
        """

        if operation == "+":
            if die_type in cls.dice:
                cls.dice[die_type] += n
            else:
                cls.dice[die_type] = n
        if operation == "-":
            if die_type in cls.dice:
                cls.dice[die_type] -= n
            else:
                # if key not in dict then subtracting dice does nothing
                pass
        if operation == "=":
            cls.dice[die_type] = n

        # final check, prunes any dice with less than one in number
        # to make sure dictionary is in a valid state
        to_delete = []
        for check_die_type, check_die_amt in cls.dice.items():
            if int(check_die_amt) < 1:
                to_delete.append(check_die_type)

        for i in to_delete:
            cls.dice.pop(i)

    @classmethod
    def clear_die_pool(cls):
        """
        Empties the dice dictionary and resets params relevant
        to dice pool (drops, success and reroll threshold)
        """
        cls.dice.clear()
        cls.success_threshold = 1
        cls.num_drops = 0
        cls.reroll_threshold = 0

    @classmethod
    def get_total_dice(cls):
        """
        Returns total dice currently in pool.
        """
        result = 0

        if cls.dice:
            result = sum(cls.dice.values())
        return result

    @classmethod
    def drop_dice(cls, roll):
        """
        Drops highest or lowest dice from the list roll, using the current
        drop mode in current Simulator config, then returns amended list roll.
        Necessary for: perform_roll().
        """
        if cls.mode_drop != "Do not drop":
            # convention for index variable that is otherwise unused
            for _ in range(cls.num_drops):
                if cls.mode_drop == "Drop lowest":
                    roll.remove(min(roll))
                elif cls.mode_drop == "Drop highest":
                    roll.remove(max(roll))
        return roll

    @classmethod
    def calculate_MoE(cls):
        """
        Calculates the approximate margin of error for each outcome
        in percentage points (not percents!) using the expected CI
        (conservative estimate using binom dist, p=0.5) based on num of trials.
        """
        moe = math.sqrt(0.5 * 0.5 / cls.num_trials)
        moe = moe * 100 * cfg.ZSTAR_VALS[cls.CI_level]

        # Display MoE to the nearest tenth of a percentage point
        return round(moe, 1)

    @classmethod
    def generate_dice_str_from_pool(cls):
        """
        Generates a string from the current dice pool in 1d2+3d4 format.
        """
        dice_str = ""
        for die_type, die_amt in cls.dice.items():
            dice_str += f"+{die_amt}d{die_type}"
        # Removes leading '+'
        return dice_str[1:]

    @classmethod
    def perform_roll(cls):
        """
        Performs a single roll with current dice in dictionary, rerolling and
                dropping dice as applicable based on current Simulator attributes, then
                returns a list of the die outcomes.
        Requires: drop_dice()
        Necessary for: perform_sim()
        """
        single_roll = []
        next_result = 0

        # Performs roll and rerolls dice until above reroll threshold
        for die_type, die_amt in cls.dice.items():
            for _ in range(die_amt):
                while True:
                    # +1 here since dice values are in form [1, n], not [1, n)
                    next_result = rand.randrange(1, die_type + 1)
                    # Strict inequality as reroll treshold defined as the highest
                    #  value that needs to be rerolled
                    if next_result > cls.reroll_threshold:
                        break
                single_roll.append(next_result)

        # Drops appropriate number of dice
        single_roll = cls.drop_dice(single_roll)

        return single_roll

    @classmethod
    def get_successes(cls, roll):
        """
        Returns the number of successes in roll based on the success threshold
        in the current Simulator configuration.
        Necessary for: perform_sim()
        """
        successes = 0
        for outcome in roll:
            if outcome >= cls.success_threshold:
                successes += 1
        return successes

    @classmethod
    def perform_sim(cls):
        """
        Performs a simulation run of number of trials stored in Simulator,
        tallying outcome frequencies to Simulator's frequency dict.
        Requires: perform_roll(), get_successes()
        """
        rand.seed()
        # Resets frequency dictionary from any past simulation run(s)
        cls.freq.clear()
        single_roll = []

        # Using this range instead of (0, t) for accurate simulation count
        for _ in range(1, cls.num_trials + 1):
            single_roll = cls.perform_roll()

            if cls.mode == "Sum":
                outcome = sum(single_roll)
            elif cls.mode == "Successes":
                outcome = cls.get_successes(single_roll)

            if outcome in cls.freq:
                cls.freq[outcome] += 1
            else:
                # Create entry outcome if outcome not yet recorded in dictionary
                cls.freq[outcome] = 1

    @classmethod
    def sanitize_outcomes(cls):
        """
        Modifies frequency dictionary:
        - changes values from counts to percents.
        - removes outcomes if associated probability is below cutoff threshold
          calculated by config's cutoff sensitivity.
        """
        to_delete = []

        # Pruning data values based on cutoff threshold
        cutoff_threshold = max(cls.freq.values()) / cfg.CUTOFF_SENSITIVITY
        for outcome, frequency in cls.freq.items():
            if frequency < cutoff_threshold:
                to_delete.append(outcome)

        for outcome in to_delete:
            cls.freq.pop(outcome)

        # Convert to percentages, round to avoid floating point inccuracies
        for outcome in cls.freq:
            cls.freq[outcome] = round(
                cls.freq[outcome] / cls.num_trials * 100, cfg.ROUNDING_PREC
            )
