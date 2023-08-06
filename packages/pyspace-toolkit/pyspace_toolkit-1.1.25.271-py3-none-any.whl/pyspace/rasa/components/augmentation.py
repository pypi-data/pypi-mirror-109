
# %%
import re
import os
from typing import Any, Dict, List, Optional, Text, Union, Type

# %%
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import SparseFeaturizer
from rasa.nlu.training_data import Message, TrainingData

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

from rasa.nlu.config import RasaNLUModelConfig

import rasa.utils.io as io_utils
from rasa.nlu import utils
import rasa.utils.common as common_utils
from rasa.nlu.model import Metadata

# %%
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

from pyspace.nlp.task.date_extractor import DateParser

from pyspace.rasa.components.data_management import TrainingDataManager

# %%
import copy
import pickle

from rasa.core.domain import Domain
from pathlib import Path

import random

from pyspace.nlp.toolkit.spacy import SpacyNLP
from pyspace.other.multiprocessing_wrapper import MultiprocessingWrapper

try:
    import nlpaug
    import nlpaug.augmenter.word as naw
    import nlpaug.augmenter.char as nac
    nlpaug_bool = True
except:
    nlpaug_bool = False

class TypoAugmentation(Component):
    defaults = {
        "word_swap_count": 3,
        "word_delete_count": 3,
        "word_split_count": 4,
        "char_delete_count": 5,
        "char_keyboard_count": 10,
        "char_swap_count": 10,
        "char_insert_count": 5,
    }

    def __init__(self, component_config: Dict[Text, Any] = None, response_dict=None) -> None:
        super(TypoAugmentation, self).__init__(component_config)
        
        self.aug_word_swap = naw.RandomWordAug(action="swap")
        self.aug_word_delete = naw.RandomWordAug(action="delete")
        self.aug_word_split = naw.SplitAug()

        self.aug_char_delete   = nac.RandomCharAug(name='delete',action="delete", aug_word_p=0.7, aug_char_p=0.3, aug_char_max=1)
        self.aug_char_keyboard_loweralpha = nac.KeyboardAug(name='keyboard', aug_word_p=0.7, aug_char_p=0.34, aug_char_max=1, include_upper_case=False, include_numeric=False, include_special_char=False)
        self.aug_char_swap     = nac.RandomCharAug(name='swap',action="swap", aug_word_p=0.7, aug_char_p=0.34, aug_char_max=2 )
        self.aug_char_insert_loweralpha   = nac.RandomCharAug(name='insert_lower',action="insert", aug_word_p=0.7, aug_char_p=0.3, aug_char_max=1, include_upper_case= False, include_numeric=False, spec_char='')


        # config = {
        #     'embedding_model':False,
        #     'whitespace_normalizer':True,
        #     'token_patterns':[], 
        #     'replace_patterns':[],
            
        #     'post_tokenization_bool':True,
        #     'post_tokenization_merge_bool':False, 
        #     'emoji_bool':False,
        #     'stanza_bool':False,

        #     'matchers':[],
        #     'phrasematchers':[],
        # }
        # self.nlp = SpacyNLP(config)
        pass


    def _mp_func(self, message):
        examples_i = []

        text = message.text
        intent = message.get(INTENT)

        temp = []
        temp += self.aug_word_swap.augment(text, n=self.component_config["word_swap_count"])
        temp += self.aug_word_delete.augment(text, n=self.component_config["word_delete_count"])
        temp += self.aug_word_split.augment(text, n=self.component_config["word_split_count"])
        temp += self.aug_char_delete.augment(text, n=self.component_config["char_delete_count"])
        temp += self.aug_char_keyboard_loweralpha.augment(text, n=self.component_config["char_keyboard_count"])
        temp += self.aug_char_swap.augment(text, n=self.component_config["char_swap_count"])
        temp += self.aug_char_insert_loweralpha.augment(text, n=self.component_config["char_insert_count"])

        for augmented_text in temp:
            augmented_example = Message(augmented_text, {INTENT:intent, ENTITIES: []})
            examples_i.append(augmented_example)
        return examples_i


    def generate_examples(self, training_data):

        # augmented_examples = []

        mp = MultiprocessingWrapper(self._mp_func, [], log_module= 100, njobs=40)
        augmented_examples = sum(mp.mp_func(training_data.training_examples), [])

        return augmented_examples



    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        augmented_examples = self.generate_examples(training_data)
        training_data.training_examples = training_data.training_examples + augmented_examples

        TrainingDataManager.reset_lazy_attributes(training_data)
        