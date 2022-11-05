from semithuesystem.alphabet import Alphabet
from semithuesystem.rules_dictionary import RulesDictionary
from typing import TypedDict
from os import path

Rule = TypedDict("Rule", { "if": str, "play": str })

class ConductingDictionary(RulesDictionary):
    AUDIO_EXTENSIONS = [".mp3"]

    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    @staticmethod
    def valid_audio(audio: str):
        return path.isfile(audio) and path.splitext(audio)[1] in ConductingDictionary.AUDIO_EXTENSIONS

    def _initialize_dictionary(self):
        for symbol in self._alphabet.symbols:
            self._dictionary[symbol] = ""

    def register(self, rule: Rule):
        if not self._alphabet.has(rule["if"]):
            raise Exception("The symbol {} is not in the alphabet".format(rule["if"]))
        
        if not ConductingDictionary.valid_audio(rule["play"]):
            raise Exception("The audio file {} is not valid".format(rule["play"]))

        self._dictionary[rule["if"]] = rule["play"]

        return self

if __name__ == "__main__":
    alphabet = Alphabet({ "A", "B", "C" })
    conducting_dictionary = ConductingDictionary(alphabet)
    
    print(conducting_dictionary.dictionary)
    
    conducting_dictionary.register({
        "if": "A",
        "play": path.join(".tmp", "B.mp3")
    })

