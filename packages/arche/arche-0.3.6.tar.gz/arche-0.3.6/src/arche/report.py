from functools import partial
from typing import Dict

from arche import SH_URL
from arche.rules.result import Level, Outcome, Result
from colorama import Fore, Style
from IPython.display import display_markdown
import numpy as np
import pandas as pd
import plotly.io as pio

display_markdown = partial(display_markdown, raw=True)


class Report:
    def __init__(self):
        self.results: Dict[str, Result] = {}

    def save(self, result: Result) -> None:
        self.results[result.name] = result

    @staticmethod
    def write_color_text(text: str, color: Fore = Fore.RED) -> None:
        print(color + text + Style.RESET_ALL)

    @staticmethod
    def write_rule_name(rule_name: str) -> None:
        display_markdown(f"{rule_name}:")

    @classmethod
    def write(cls, text: str) -> None:
        print(text)

    def write_summaries(self) -> None:
        for result in self.results.values():
            self.write_summary(result)

    @classmethod
    def write_summary(cls, result: Result) -> None:
        cls.write_rule_name(result.name)
        if not result.messages:
            cls.write_rule_outcome(Outcome.PASSED, Level.INFO)
        for level, rule_msgs in result.messages.items():
            for rule_msg in rule_msgs:
                cls.write_rule_outcome(rule_msg.summary, level)

    @classmethod
    def write_rule_outcome(cls, outcome: str, level: Level = Level.INFO) -> None:
        if isinstance(outcome, Outcome):
            outcome = outcome.name
        msg = f"\t{outcome}"
        if level == Level.ERROR:
            cls.write_color_text(msg)
        elif level == Level.WARNING:
            cls.write_color_text(msg, color=Fore.YELLOW)
        elif outcome == Outcome.PASSED.name:
            cls.write_color_text(msg, color=Fore.GREEN)
        else:
            cls.write(msg)

    def write_details(self, short: bool = False, keys_limit: int = 10) -> None:
        for result in self.results.values():
            if result.detailed_messages_count:
                display_markdown(
                    f"{result.name} ({result.detailed_messages_count} message(s)):"
                )
                self.write_rule_details(result, short, keys_limit)
            for f in result.figures:
                pio.show(f)
            display_markdown("<br>")

    @classmethod
    def write_rule_details(
        cls, result: Result, short: bool = False, keys_limit: int = 10
    ) -> None:
        for rule_msgs in result.messages.values():
            for rule_msg in rule_msgs:
                if rule_msg.errors:
                    cls.write_detailed_errors(rule_msg.errors, short, keys_limit)
                elif rule_msg.detailed:
                    cls.write(rule_msg.detailed)

    @classmethod
    def write_detailed_errors(cls, errors: Dict, short: bool, keys_limit: int) -> None:
        if short:
            keys_limit = 5
            error_messages = list(errors.items())[:5]
        else:
            error_messages = list(errors.items())
        for attribute, keys in error_messages:
            if isinstance(keys, list):
                keys = pd.Series(keys)
            if isinstance(keys, set):
                keys = pd.Series(list(keys))

            sample = Report.sample_keys(keys, keys_limit)
            display_markdown(
                f"{len(keys)} items affected - {attribute}: {sample}", raw=True
            )

    @staticmethod
    def sample_keys(keys: pd.Series, limit: int) -> str:
        if len(keys) > limit:
            sample = keys.sample(limit)
        else:
            sample = keys

        def url(x: str) -> str:
            if SH_URL in x:
                return f"[{x.split('/')[-1]}]({x})"
            key, number = x.rsplit("/", 1)
            return f"[{number}]({SH_URL}/{key}/item/{number})"

        # make links only for Cloud data
        if keys.dtype == np.dtype("object") and "/" in keys.iloc[0]:
            sample = sample.apply(url)

        return ", ".join(sample.apply(str))
