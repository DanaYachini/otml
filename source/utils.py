import re
import logging
from datetime import timedelta


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

def select_worst_idx(population, k, fit_attr="fitness"):
    """ Same as DEAP.selection.selWorst() but returns selected indices  """
    zipped = list(zip(population, list(range(len(population)))))
    worst = sorted(zipped, key=lambda tup: attrgetter(fit_attr)(tup[0]))[:k]
    return [tup[1] for tup in worst]

def log_hypothesis(logger, hypothesis):
    logger.info("Grammar with: {}:".format(hypothesis.grammar.constraint_set))
    logger.info("{}".format(hypothesis.grammar.lexicon))
    logger.info("Parse: {}".format(hypothesis.get_recent_data_parse()))
    logger.info(hypothesis.get_recent_energy_signature())
