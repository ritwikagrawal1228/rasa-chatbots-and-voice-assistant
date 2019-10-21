import numpy as np
import typing
from typing import Any

from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.featurizers.featurzier import Featurizer
from rasa.nlu.training_data import Message, TrainingData

if typing.TYPE_CHECKING:
    from spacy.language import Language
    from spacy.tokens import Doc

from rasa.nlu.constants import (
    MESSAGE_TEXT_ATTRIBUTE,
    MESSAGE_SPACY_FEATURES_NAMES,
    MESSAGE_VECTOR_DENSE_FEATURE_NAMES,
    SPACY_FEATURIZABLE_ATTRIBUTES,
)


def ndim(spacy_nlp: "Language") -> int:
    """Number of features used to represent a document / sentence."""
    return spacy_nlp.vocab.vectors_length


def features_for_doc(doc: "Doc") -> np.ndarray:
    """Feature vector for a single document / sentence."""
    return doc.vector


class SpacyFeaturizer(Featurizer):

    provides = [
        MESSAGE_VECTOR_DENSE_FEATURE_NAMES[attribute]
        for attribute in SPACY_FEATURIZABLE_ATTRIBUTES
    ]

    requires = [
        MESSAGE_SPACY_FEATURES_NAMES[attribute]
        for attribute in SPACY_FEATURIZABLE_ATTRIBUTES
    ]

    def train(
        self, training_data: TrainingData, config: RasaNLUModelConfig, **kwargs: Any
    ) -> None:

        for example in training_data.intent_examples:
            for attribute in SPACY_FEATURIZABLE_ATTRIBUTES:
                self._set_spacy_features(example, attribute)

    def get_doc(self, message, attribute):

        return message.get(MESSAGE_SPACY_FEATURES_NAMES[attribute])

    def process(self, message: Message, **kwargs: Any) -> None:

        self._set_spacy_features(message)

    def _set_spacy_features(self, message, attribute=MESSAGE_TEXT_ATTRIBUTE):
        """Adds the spacy word vectors to the messages features."""

        message_attribute_doc = self.get_doc(message, attribute)
        if message_attribute_doc is not None:
            fs = features_for_doc(message_attribute_doc)
            features = self._combine_with_existing_dense_features(
                message, fs, MESSAGE_VECTOR_DENSE_FEATURE_NAMES[attribute]
            )
            message.set(MESSAGE_VECTOR_DENSE_FEATURE_NAMES[attribute], features)
