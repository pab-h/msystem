from os import path

from semithuesystem.semi_thue_system import SemiThueSystem
from semithuesystem.rules_dictionary import RulesDictionary
from semithuesystem.alphabet import Alphabet

from msystem.conducting_dictionary import ConductingDictionary

from pydub import AudioSegment
from pydub import playback

class MSystem(SemiThueSystem):
    def __init__(self, axiom: str, rules_dictionary: RulesDictionary, conducting_dictionary: ConductingDictionary):
        super().__init__(axiom, rules_dictionary)

        if rules_dictionary.alphabet != conducting_dictionary.alphabet:
            raise Exception("The rule dictionary alphabet and the conducting dictionary alphabet are not the same")

        self._conducting = conducting_dictionary.dictionary

    def to_score(self) -> str:
        return "".join(self._interactions)

    def perform(self): 
        def play_note(note: str):
            if self._conducting[note]:
                note = AudioSegment.from_file(self._conducting[note])
                playback.play(note)

        list(map(play_note, list(self.to_score())))
 

alphabet = Alphabet({ "A", "B", "C" })

rules = RulesDictionary(alphabet)
rules.register({ "of": "A", "to": "B"})
rules.register({ "of": "B", "to": "CA"})

conducting = ConductingDictionary(alphabet)
conducting.register({ "if": "A", "play": path.join(".tmp", "B.mp3") })

msystem = MSystem("AAA", rules, conducting)

msystem.interact()
msystem.interact()
msystem.interact()
msystem.interact()

msystem.perform()
