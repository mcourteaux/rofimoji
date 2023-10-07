from subprocess import run
from typing import Dict, List, Tuple, Union

from ..abstractionhelper import is_installed
from ..models import CANCEL, DEFAULT, Action, Shortcut
from .selector import Selector


class DMenu(Selector):
    @staticmethod
    def supported() -> bool:
        return is_installed("dmenu")

    @staticmethod
    def name() -> str:
        return "dmenu"

    def show_character_selection(
        self,
        characters: List[str],
        recent_characters: List[str],
        prompt: str,
        keybindings: Dict[Action, str],
        additional_args: List[str],
    ) -> Tuple[Union[Action, DEFAULT, CANCEL], Union[List[str], Shortcut]]:
        parameters = ["dmenu", "-i", "-p", prompt, *additional_args]

        dmenu = run(parameters, input="\n".join(characters), capture_output=True, encoding="utf-8")
        return DEFAULT(), [self.extract_char_from_input(line) for line in dmenu.stdout.splitlines()]

    def show_skin_tone_selection(
        self, tones_emojis: List[str], prompt: str, additional_args: List[str]
    ) -> Tuple[int, str]:
        dmenu = run(
            ["dmenu", "-p", prompt, *additional_args],
            input="\n".join(tones_emojis),
            capture_output=True,
            encoding="utf-8",
        )

        return dmenu.returncode, dmenu.stdout

    def show_action_menu(self, additional_args: List[str]) -> List[Action]:
        dmenu = run(
            [
                "dmenu",
                *additional_args,
            ],
            input="\n".join([it.value for it in Action if it != Action.MENU]),
            capture_output=True,
            encoding="utf-8",
        )

        return [Action(dmenu.stdout.strip())]