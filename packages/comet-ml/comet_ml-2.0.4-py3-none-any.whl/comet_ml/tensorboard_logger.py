# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2019 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************


import logging

from comet_ml._logging import check_module

LOGGER = logging.getLogger(__name__)
DISABLED = False


def extract_from_add_summary(file_writer, summary, global_step):
    from tensorflow.core.framework import summary_pb2

    extracted_values = {}

    if isinstance(summary, bytes):
        summ = summary_pb2.Summary()
        summ.ParseFromString(summary)
        summary = summ

    for value in summary.value:
        field = value.WhichOneof("value")

        if field == "simple_value":
            extracted_values[value.tag] = value.simple_value

    return extracted_values, global_step


def add_summary_logger(experiment, original, value, *args, **kwargs):
    try:
        if DISABLED is False:

            LOGGER.debug("TENSORBOARD LOGGER CALLED")
            params, step = extract_from_add_summary(*args, **kwargs)
            experiment.log_metrics(params, step=step)

    except Exception:
        LOGGER.error("Failed to extract parameters from add_summary()", exc_info=True)


class ContextHolder:
    def __init__(self, new_context):
        self.new_context = new_context
        self.old_context = None

    def enter(self, experiment, *args, **kwargs):
        self.old_context = experiment.context
        experiment.context = self.new_context

    def exit(self, experiment, *args, **kwargs):
        experiment.context = self.old_context
        self.old_context = None


ADD_SUMMARY = [
    (
        "tensorflow.python.summary.writer.writer",
        "SummaryToEventTransformer.add_summary",
    ),
    ("tensorflow.summary", "FileWriter.add_summary"),
]

TRAIN_HOLDER = ContextHolder("train")
EVAL_HOLDER = ContextHolder("eval")


def patch(module_finder):
    check_module("tensorflow")
    check_module("tensorboard")

    # Register the fit methods
    for module, object_name in ADD_SUMMARY:
        module_finder.register_after(module, object_name, add_summary_logger)
    module_finder.register_before(
        "tensorflow.python.estimator.estimator", "Estimator.train", TRAIN_HOLDER.enter
    )
    module_finder.register_after(
        "tensorflow.python.estimator.estimator", "Estimator.train", TRAIN_HOLDER.exit
    )
    module_finder.register_before(
        "tensorflow_estimator.python.estimator.estimator",
        "Estimator.train",
        TRAIN_HOLDER.enter,
    )
    module_finder.register_after(
        "tensorflow_estimator.python.estimator.estimator",
        "Estimator.train",
        TRAIN_HOLDER.exit,
    )
    module_finder.register_before(
        "tensorflow.python.estimator.estimator", "Estimator.evaluate", EVAL_HOLDER.enter
    )
    module_finder.register_after(
        "tensorflow.python.estimator.estimator", "Estimator.evaluate", EVAL_HOLDER.exit
    )
    module_finder.register_before(
        "tensorflow_estimator.python.estimator.estimator",
        "Estimator.evaluate",
        EVAL_HOLDER.enter,
    )
    module_finder.register_after(
        "tensorflow_estimator.python.estimator.estimator",
        "Estimator.evaluate",
        EVAL_HOLDER.exit,
    )


check_module("tensorflow")
check_module("tensorboard")
