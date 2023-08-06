from typing import Sequence, Optional, Union, Any, Dict
import functools

import tensorflow as tf
from tensorflow.keras.metrics import Precision, Recall
from tensorflow_addons.metrics import FBetaScore


class PrecisionWithLogits(Precision):
    def __init__(
        self,
        thresholds: Union[float, Sequence[float], None] = None,
        top_k: Optional[int] = None,
        class_id: Optional[int] = None,
        name: str = "precision",
        dtype: Optional[tf.DType] = None,
        is_multilabel: bool = False,
    ) -> None:
        if thresholds is None:
            thresholds = 0 if is_multilabel else 0.5
        super().__init__(
            thresholds=thresholds,
            top_k=top_k,
            class_id=class_id,
            name=name,
            dtype=dtype,
        )
        self.is_multilabel = is_multilabel

    def update_state(
        self,
        y_true: tf.Tensor,
        y_logits: tf.Tensor,
        sample_weight: Optional[tf.Tensor] = None,
    ) -> None:
        if self.is_multilabel:
            y_logits = y_logits >= self.thresholds
        else:
            y_logits = tf.math.softmax(y_logits, axis=-1)
        super().update_state(y_true, y_logits, sample_weight=sample_weight)

    def get_config(self) -> Dict[str, Any]:
        return {**super().get_config(), "is_multilabel": self.is_multilabel}


class RecallWithLogits(Recall):
    def __init__(
        self,
        thresholds: Union[float, Sequence[float], None] = None,
        top_k: Optional[int] = None,
        class_id: Optional[int] = None,
        name: str = "recall",
        dtype: Optional[tf.DType] = None,
        is_multilabel: bool = False,
    ) -> None:
        if thresholds is None:
            thresholds = 0 if is_multilabel else 0.5
        super().__init__(
            thresholds=thresholds,
            top_k=top_k,
            class_id=class_id,
            name=name,
            dtype=dtype,
        )
        self.is_multilabel = is_multilabel

    def update_state(
        self,
        y_true: tf.Tensor,
        y_logits: tf.Tensor,
        sample_weight: Optional[tf.Tensor] = None,
    ) -> None:
        if self.is_multilabel:
            y_logits = y_logits >= self.thresholds
        else:
            y_logits = tf.math.softmax(y_logits, axis=-1)
        super().update_state(y_true, y_logits, sample_weight=sample_weight)

    def get_config(self) -> Dict[str, Any]:
        return {**super().get_config(), "is_multilabel": self.is_multilabel}


class FBetaScoreWithLogits(FBetaScore):
    def __init__(
        self,
        num_classes: int,
        average: str = "micro",
        beta: float = 1.0,
        thresholds: Optional[float] = None,
        name: str = "fbeta_score",
        dtype: Optional[tf.DType] = None,
        is_multilabel: bool = False,
    ) -> None:
        if thresholds is None:
            thresholds = 0 if is_multilabel else 0.5
        super().__init__(
            num_classes,
            average=average,
            beta=beta,
            threshold=thresholds,
            name=name,
            dtype=dtype,
        )
        self.is_multilabel = is_multilabel

    def update_state(
        self,
        y_true: tf.Tensor,
        y_logits: tf.Tensor,
        sample_weight: Optional[tf.Tensor] = None,
    ) -> None:
        if self.is_multilabel:
            y_logits = y_logits >= self.thresholds
        else:
            y_logits = tf.math.softmax(y_logits, axis=-1)
        super().update_state(y_true, y_logits, sample_weight=sample_weight)

    def get_config(self) -> Dict[str, Any]:
        configs = super().get_config()
        configs.pop("threshold", None)
        return {
            **configs,
            "is_multilabel": self.is_multilabel,
            "thresholds": self.threshold,
        }