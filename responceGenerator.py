from section import Section
import pandas as pd
import json


class ResponceGenerator():
    def __init__(self):
        self.sections: list[Section] = []

    def addSection(self, section: Section):
        self.sections.append(section)

    def calculate(self, data: pd.DataFrame):
        for section in self.sections:
            section.calculate(data)

    def produceJson(self) -> str:
        return json.dumps({section.name: section.getData() for section in self.sections}, indent=4)