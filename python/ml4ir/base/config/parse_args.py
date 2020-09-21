from argparse import ArgumentParser, Namespace
from typing import List


class RelevanceArgParser(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.define_args()
        self.set_default_args()

    def define_args(self):
        self.add_argument(
            "--data_dir",
            type=str,
            default=None,
            help="Path to the data directory to be used for training and inference. "
            "Can optionally include train/ val/ and test/ subdirectories. "
            "If subdirectories are not present, data will be split based on train_pcent_split",
        )

        self.add_argument(
            "--data_format",
            type=str,
            default="tfrecord",
            help="Format of the data to be used. "
            "Should be one of the Data format keys in ml4ir/config/keys.py",
        )

        self.add_argument(
            "--tfrecord_type",
            type=str,
            default="example",
            help="TFRecord type of the data to be used. "
            "Should be one of the TFRecord type keys in ml4ir/config/keys.py",
        )

        self.add_argument(
            "--feature_config",
            type=str,
            default=None,
            help="Path to YAML file or YAML string with feature metadata for training.",
        )

        self.add_argument(
            "--model_file",
            type=str,
            default="",
            help="Path to a pretrained model to load for either resuming training or for running in"
            "inference mode.",
        )

        self.add_argument(
            "--model_config",
            type=str,
            default="ml4ir/base/config/default_model_config.yaml",
            help="Path to the Model config YAML used to build the model architecture.",
        )

        self.add_argument(
            "--optimizer_key",
            type=str,
            default="adam",
            help="Optimizer to use. Has to be one of the optimizers in OptimizerKey under "
            "ml4ir/config/keys.py",
        )

        self.add_argument(
            "--loss_key",
            type=str,
            default=None,
            help="Loss to optimize. Has to be one of the losses in LossKey under ml4ir/config/keys.py",
        )

        self.add_argument(
            "--metrics_keys",
            type=str,
            default=None,
            help="Metric to compute. Can be a list. Has to be one of the metrics in MetricKey under "
            "ml4ir/config/keys.py",
        )

        self.add_argument(
            "--monitor_metric",
            type=str,
            default=None,
            help="Metric name to use for monitoring training loop in callbacks"
            "ml4ir/config/keys.py",
        )

        self.add_argument(
            "--monitor_mode",
            type=str,
            default=None,
            help="Metric mode to use for monitoring training loop in callbacks",
        )

        self.add_argument(
            "--num_epochs",
            type=int,
            default=5,
            help="Max number of training epochs(or full pass over the data)",
        )

        self.add_argument(
            "--batch_size", type=int, default=128, help="Number of data samples to use per batch."
        )

        self.add_argument(
            "--learning_rate", type=float, default=0.01, help="Step size (e.g.: 0.01)"
        )

        self.add_argument(
            "--learning_rate_decay",
            type=float,
            default=0.90,
            help="decay rate for the learning rate",
        )

        self.add_argument(
            "--learning_rate_decay_steps",
            type=int,
            default=1000,
            help="decay rate for the learning rate",
        )

        self.add_argument(
            "--compute_intermediate_stats",
            type=bool,
            default=True,
            help="Whether to compute intermediate stats on test set (mrr, acr, etc) (slow)",
        )

        self.add_argument(
            "--execution_mode",
            type=str,
            default="train_inference_evaluate",
            help="Execution mode for the pipeline. Should be one of ExecutionModeKey",
        )

        self.add_argument(
            "--random_state",
            type=int,
            default=123,
            help="Initialize the seed to control randomness for replication",
        )

        self.add_argument(
            "--run_id",
            type=str,
            default="",
            help="Unique string identifier for the current training run. Used to identify logs and models directories. Autogenerated if not specified.",
        )

        self.add_argument(
            "--run_group",
            type=str,
            default="general",
            help="Unique string identifier to group multiple model training runs. Allows for defining a meta grouping to filter different model training runs for best model selection as a post step.",
        )

        self.add_argument(
            "--run_notes",
            type=str,
            default="",
            help="Notes for the current training run. Use this argument to add short description of the model training run that helps in identifying the run later.",
        )

        self.add_argument(
            "--models_dir",
            type=str,
            default="models/",
            help="Path to save the model. Will be expanded to models_dir/run_id",
        )

        self.add_argument(
            "--logs_dir",
            type=str,
            default="logs/",
            help="Path to save the training/inference logs. Will be expanded to logs_dir/run_id",
        )

        self.add_argument(
            "--checkpoint_model",
            type=bool,
            default=True,
            help="Whether to save model checkpoints at the end of each epoch. Recommended - set to True",
        )

        self.add_argument(
            "--train_pcent_split",
            type=float,
            default=0.8,
            help="Percentage of all data to be used for training. The remaining is used for validation and "
            "testing. Remaining data is split in half if val_pcent_split or test_pcent_split are not "
            "specified.",
        )

        self.add_argument(
            "--val_pcent_split",
            type=float,
            default=-1,
            help="Percentage of all data to be used for testing.",
        )

        self.add_argument(
            "--test_pcent_split",
            type=float,
            default=-1,
            help="Percentage of all data to be used for testing.",
        )

        self.add_argument(
            "--max_sequence_size",
            type=int,
            default=0,
            help="Maximum number of elements per sequence feature.",
        )

        self.add_argument(
            "--inference_signature",
            type=str,
            default="serving_default",
            help="SavedModel signature to be used for inference",
        )

        self.add_argument(
            "--use_part_files",
            type=bool,
            default=False,
            help="Whether to look for part files while loading data",
        )

        self.add_argument(
            "--logging_frequency",
            type=int,
            default=25,
            help="How often to log results to log file. Int representing number of batches.",
        )

        self.add_argument(
            "--group_metrics_min_queries",
            type=int,
            default=None,
            help="Minimum number of queries per group to be used to computed groupwise metrics.",
        )

        self.add_argument(
            "--gradient_clip_value",
            type=float,
            default=5.0,
            help="Gradient clipping value/threshold for the optimizer.",
        )

        self.add_argument(
            "--compile_keras_model",
            type=bool,
            default=False,
            help="Whether to compile a loaded SavedModel into a Keras model. "
            "NOTE: This requires that the SavedModel's architecture, loss, metrics, etc are the same as the RankingModel"
            "If that is not the case, then you can still use a SavedModel from a model_file for inference/evaluation only",
        )

        self.add_argument(
            "--use_all_fields_at_inference",
            type=bool,
            default=False,
            help="Whether to require all fields in the serving signature of the SavedModel. If set to False, only requires fields with required_only=True",
        )

        self.add_argument(
            "--pad_sequence_at_inference",
            type=bool,
            default=False,
            help="Whether to pad sequence at inference time. Used to define the TFRecord serving signature in the SavedModel",
        )

        self.add_argument(
            "--output_name",
            type=str,
            default="relevance_score",
            help="Name of the output node of the model",
        )

        self.add_argument(
            "--early_stopping_patience",
            type=int,
            default=2,
            help="How many epochs to wait before early stopping on metric degradation",
        )

        self.add_argument(
            "--file_handler",
            type=str,
            default="local",
            help="String specifying the file handler to be used. Should be one of FileHandler keys in ml4ir/base/config/keys.py",
        )

        self.add_argument(
            "--track_experiment",
            type=bool,
            default=False,
            help="Whether to track model performance and hyperparameters.",
        )

    def set_default_args(self):
        pass


def get_args(args: List[str]) -> Namespace:
    return RelevanceArgParser().parse_args(args)
