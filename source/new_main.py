import codecs
from logging import StreamHandler
import logging
from otml_configuration_manager import OtmlConfigurationManager
from pathlib import Path

current_file_path = Path(__file__)
source_directory_path = current_file_path.parent
fixtures_directory_path = Path(source_directory_path, "tests", "fixtures")


RUN_NAME = "bb_only_delete_segment_configuration__2024_03_07"
FEATURE_TABLE_FILE_NAME = "a_b_and_cons_feature_table.json"
CORPUS_FILE_NAME = "bb_corpus.txt"
CONSTRAINT_SET_FILE_NAME = "bb_target_constraint_set.json"
CONFIGURATION_FILE_NAME = "bb_only_delete_segment_configuration.json"


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
#print(grammar.get_encoding_length())



#print(grammar.get_all_outputs_grammar())

#data = corpus.get_words()
data = grammar.get_all_outputs_grammar()
traversable_hypothesis = TraversableGrammarHypothesis(grammar, data)

print(traversable_hypothesis.get_energy())

simulated_annealing = SimulatedAnnealing(traversable_hypothesis)
simulated_annealing.run()

# 412,494 bits (Grammar = 9,294) + (Data = 403,200)


# 407,274 bits (Grammar = 4,074) + (Data = 403,200)