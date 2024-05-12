import codecs
from logging import StreamHandler
import logging
from otml_configuration_manager import OtmlConfigurationManager
from pathlib import Path

current_file_path = Path(__file__)
source_directory_path = current_file_path.parent
fixtures_directory_path = Path(source_directory_path, "tests", "fixtures")


RUN_NAME = "ga"
FEATURE_TABLE_FILE_NAME = "a_b_and_cons_feature_table.json"
CORPUS_FILE_NAME = "bb_for_paper_corpus.txt"
CONSTRAINT_SET_FILE_NAME = "bb_constraints.json"
CONFIGURATION_FILE_NAME = "otml_ga_configuration.json"


configuration_file_path = str(Path(fixtures_directory_path, "configuration", CONFIGURATION_FILE_NAME))

configuration_json_str = codecs.open(configuration_file_path, 'r').read()
OtmlConfigurationManager(configuration_json_str)

from grammar.lexicon import Lexicon
from grammar.feature_table import FeatureTable
from grammar.constraint_set import ConstraintSet
from grammar.grammar import Grammar
from traversable_grammar_hypothesis import TraversableGrammarHypothesis
from corpus import Corpus
from simulated_annealing import SimulatedAnnealing
from genetic_algorithm import GeneticAlgoritm
logging_directory_path = Path(source_directory_path, "logging")

log_file_path = str(Path(logging_directory_path, "ab.txt"))


logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s", "%Y-%m-%d %H:%M:%S")
file_log_handler = logging.FileHandler(log_file_path, mode='w')
file_log_handler.setFormatter(file_log_formatter)
logger.addHandler(file_log_handler)

console_handler = StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(file_log_formatter)
logger.addHandler(console_handler)


feature_table_file_path = str(Path(fixtures_directory_path, "feature_table", FEATURE_TABLE_FILE_NAME))
corpus_file_path = str(Path(fixtures_directory_path, "corpora", CORPUS_FILE_NAME))
constraint_set_file_path = str(Path(fixtures_directory_path, "constraint_sets", CONSTRAINT_SET_FILE_NAME))


configuration_json_str = codecs.open(configuration_file_path, 'r').read()
OtmlConfigurationManager(configuration_json_str)

feature_table = FeatureTable.load(feature_table_file_path)
corpus = Corpus.load(corpus_file_path)
constraint_set = ConstraintSet.load(constraint_set_file_path, feature_table)
lexicon = Lexicon(corpus.get_words(), feature_table)
grammar = Grammar(feature_table, constraint_set, lexicon)
data = grammar.get_all_outputs_grammar()

ga = GeneticAlgoritm(data, grammar)
res_ga = ga.run()

traversable_hypothesis = TraversableGrammarHypothesis(grammar, data)
# print(traversable_hypothesis.get_energy())

simulated_annealing = SimulatedAnnealing(traversable_hypothesis)
sa_res = simulated_annealing.run()[1]
print("BASE:", traversable_hypothesis.get_energy())
print("GA: ", res_ga.get_energy())
print("SA: ", sa_res.get_energy())
