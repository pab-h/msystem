from os import path

from uuid import uuid4 as uuid

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

    @property
    def score(self) -> str:
        return "".join(self._interactions)

    def file(self, out: str = ".") -> str:
        file = AudioSegment.empty()

        for note in self.score:
            audio = AudioSegment.from_file(self._conducting[note])
            file = file.append(audio, 0)

        file_out_path = f"{ out }/msystem-result-{ uuid() }.mp3"  

        file.export(file_out_path, "mp3")

        return file_out_path

    def perform(self): 
        def play_note(note: str):
            if self._conducting[note]:
                audio = AudioSegment.from_file(self._conducting[note])
                playback.play(audio)

        list(map(play_note, list(self.score)))
 
if __name__ == "__main__":
    alphabet = Alphabet({ "A", "B"})

    rules = RulesDictionary(alphabet)
    rules.register({ "of": "A", "to": "AB"})
    rules.register({ "of": "B", "to": "A" })

    conducting = ConductingDictionary(alphabet)
    conducting.register({ "if": "A", "play": path.join(".tmp", "F.mp3")})
    conducting.register({ "if": "B", "play": path.join(".tmp", "G.mp3")})

    msystem = MSystem("A", rules, conducting)

    print("A")
    for _ in range(3):
        print(msystem.interact())

    # msystem.perform()
    print(msystem.file(path.join(".tmp")))


