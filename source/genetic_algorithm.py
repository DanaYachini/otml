from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os
from math import exp
from random import choice
import random
from datetime import timedelta
import time
import re
from otml_configuration_manager import OtmlConfigurationManager, OtmlConfigurationError
import subprocess
from grammar.grammar import Grammar
from grammar.constraint_set import ConstraintSet
from grammar.constraint import Constraint
from grammar.lexicon import Word
from mail import MailManager
from traversable_grammar_hypothesis import TraversableGrammarHypothesis

configurations = OtmlConfigurationManager.get_instance()
if configurations is None:
    raise OtmlConfigurationError("OtmlConfigurationManager was not initialized")


logger = logging.getLogger(__name__)

process_id = os.getpid()


class GeneticAlgoritm(object):
    def __init__(self, data, grammar):
        self.input_data = data
        self.input_grammar = grammar

        self.generation = 0
        self.start_time = None
        self.previous_interval_energy = None
        self.population = None

        self.max_generations = configurations["MAX_GENERATION"]
        self.population_size = configurations["POPULATION_SIZE"]
        self.elite_size = configurations["ELITE_SIZE"]
        self.mutation_rate = configurations["MUTATION_RATE"]

    def init_population(self):
        start_hypothesis = TraversableGrammarHypothesis(self.input_grammar, self.input_data)
        population = [start_hypothesis.get_neighbor()[1] for _ in range(self.population_size - 1)] + [start_hypothesis]
        self.population = population

    def run(self):
        self.init_population()
        self.start_time = time.time()
        self.previous_interval_energy = self.population[0].get_energy()
        for gen in range(self.max_generations):
            self.make_generation()
            self.generation += 1
            if not (gen + 1) % configurations["DEBUG_LOGGING_INTERVAL"]:
                self.log_hypothesis_state()

        return min(self.population, key=lambda hypothesis: hypothesis.get_energy())

    def make_generation(self):
        elite = self.get_elite()
        next_gen = self.tournenment_selection()
        offsprings = [hypothesis.get_neighbor()[1] if random.random() < self.mutation_rate else hypothesis
                      for hypothesis in next_gen]

        self.population = elite + offsprings

    def get_elite(self):
        sort_pop = sorted(self.population, key=lambda hypothesis: hypothesis.get_energy())
        return sort_pop[:self.elite_size]

    def tournenment_selection(self):
        next_gen = []
        for _ in range(self.population_size - self.elite_size):
            winner = min(random.sample(self.population, configurations["TOURNAMENT_SIZE"]),
                         key=lambda hypothesis: hypothesis.get_energy())
            next_gen.append(winner)
        return next_gen

    def log_hypothesis_state(self):
        current_time = time.time()

        logger.info("\n" + "-" * 125 + "\n")
        percentage_completed = 100 * float(self.generation) / float(self.max_generations)
        logger.info("Generation {0:,} of {1:,} ({2:.2f}%)".format(self.generation, self.max_generations,
                                                                  percentage_completed))
        logger.info("-" * 80)
        elapsed_time = current_time - self.start_time
        logger.info("Time from simulation start: {}".format(_pretty_runtime_str(elapsed_time)))
        crude_expected_time = elapsed_time * (100 / percentage_completed)
        logger.info("Expected simulation time: {} ".format(_pretty_runtime_str(crude_expected_time)))

        for hypo in self.population:
            logger.info("- " * 40)
            logger.info("Grammer with: {}:".format(hypo.grammar.constraint_set))
            if configurations["RESTRICTION_ON_ALPHABET"]:
                restricted_alphabet = hypo.grammar.lexicon.get_distinct_segments()
                restricted_alphabet_list = [segment.symbol for segment in restricted_alphabet]
                logger.info("Alphabet: {}".format(restricted_alphabet_list))
            logger.info("{}".format(hypo.grammar.lexicon))
            logger.info("Parse: {}".format(hypo.get_recent_data_parse()))
            logger.info(hypo.get_recent_energy_signature())

def _pretty_runtime_str(run_time_in_seconds):
    time_delta = timedelta(seconds=run_time_in_seconds)
    timedelta_string = str(time_delta)

    m = re.search('(\d* (days|day), )?(\d*):(\d*):(\d*)', timedelta_string)
    days_string = m.group(1)
    hours = int(m.group(3))
    minutes = int(m.group(4))
    seconds = int(m.group(5))

    if days_string:
        days_string = days_string[:-2]
        return "{}, {} hours, {} minutes, {} seconds".format(days_string, hours, minutes, seconds)
    elif hours:
        return "{} hours, {} minutes, {} seconds".format(hours, minutes, seconds)
    elif minutes:
        return "{} minutes, {} seconds".format(minutes, seconds)
    else:
        return "{} seconds".format(seconds)