import pandas as pd
import os

from M_SituationManager import SituationGenerator

class SITUATION():
    def __init__(self, Study_path: str):

        self.id: int = None
        self.name: str = None
        self.system_config: str = None
        self.timeframe: str = None
        self.rainfall: list = None
        self.db_path: str = None
        
        self.study_path = Study_path
        
        self.functional_answers: pd.DataFrame = None
        self.functional_objectives_completeness: pd.DataFrame = None
        self.functional_objectives_rating: pd.DataFrame = None
        self.functional_criteria_rating: pd.DataFrame = None
        self.functional_rating: float = 0
        
        self.system_performance_rating: pd.DataFrame = None
        self.system_performance_final_rating: float = 0
        self.system_consequences_rating: pd.DataFrame = None
        self.system_consequences_final_rating: float = 0
        
        self.performance_rating: float = 0
        
        self.overall_rating: float = 0

    def update_from_generator(self,
               SituationGenerator: SituationGenerator,
               Situation_ID: int):

        situations = SituationGenerator.get_situations_table()

        if Situation_ID == -1:
            self.id = None
            self.name = None
            self.system_config = None
            self.timeframe = None
            self.rainfall = None
        else:
            selected_situation = situations[situations['SituationID'] == Situation_ID].squeeze()
            self.id = selected_situation["SituationID"]
            self.name = selected_situation["SituationName"]
            self.system_config = selected_situation["SystemConfiguration"]
            self.timeframe = selected_situation["TimeFrame"]
            rainfall_values = selected_situation["Rainfall"].split("; ")
            self.rainfall = [int(value) for value in rainfall_values]  #list of Rainfall return periods as integers!
            self.db_path = os.path.join(self.study_path, f"{self.id}-SITUATION.db")

    def update_from_table_row(self, SituationsTableRow):
        self.id = SituationsTableRow["SituationID"]
        self.name = SituationsTableRow["SituationName"]
        self.system_config = SituationsTableRow["SystemConfiguration"]
        self.timeframe = SituationsTableRow["TimeFrame"]
        rainfall_values = SituationsTableRow["Rainfall"].split("; ")
        self.rainfall = [int(value) for value in rainfall_values]
        self.db_path = os.path.join(self.study_path, f"{self.id}-SITUATION.db")