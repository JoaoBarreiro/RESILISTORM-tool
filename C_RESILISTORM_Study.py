from PySide6.QtSql import QSqlDatabase

import os
import re
import pandas as pd
import numpy as np
import shutil

from M_WelcomeDialog import WelcomeDialog
import M_OperateDatabases
import M_SituationManager
import C_RESILISTORM_Situation

class STUDY():

    def __init__(self,
                 WelcomeDialog: WelcomeDialog,
                 Study_Database: QSqlDatabase,
                 Methodolohy_Database: QSqlDatabase):
        
        self.Name = WelcomeDialog.study_name
        self.Directory = WelcomeDialog.study_directory
        
        self.Methodology_path = None
        self.Methodology = Methodolohy_Database
        
        self.Database_path =  None
        self.Database = Study_Database
        
        self.Situations = {}      #dict of SituationID: Situation
        self.Weights = None         #dict of weights by level, as pd.Dataframe
        self.Selected_indicators = None      #pd.Dataframe
        
        refuss_contents = M_OperateDatabases.getREFUSSDatabase(self.Methodology)
        self.dimensions = refuss_contents[0]
        self.objectives = refuss_contents[1].set_index("ObjectiveID")
        self.criteria = refuss_contents[2].set_index("CriteriaID")
        self.metrics = refuss_contents[3].set_index("MetricID")
        self.metric_options = refuss_contents[4].set_index("MetricID")
        self.indicators = {'indicators_classes': refuss_contents[5].set_index("IndicatorClassID"),
                           'indicators_library': refuss_contents[6].set_index("IndicatorID")}
        
        #add short and full labels to dataframes
        self.add_labels_to_dataframes()        

        self.IndicatorsLibrary = M_OperateDatabases.fetch_table_from_database(self.Methodology, "IndicatorsLibrary")
        self.IndicatorsLibrary.set_index("IndicatorID", inplace=True)

        self.IndicatorsClassesLibrary = M_OperateDatabases.fetch_table_from_database(self.Methodology, "IndicatorsClassesLibrary")
        self.IndicatorsClassesLibrary.set_index("IndicatorClassID", inplace=True)             

        self.IndicatorsSetup = None
        
        # Automatically initialize the methodology and database paths
        self.set_files_and_paths(WelcomeDialog)

        M_OperateDatabases.establishDatabaseConnections([(self.Methodology, self.Methodology_path),
                                                         (self.Database, self.Database_path)
                                                         ])

        # Create Study Database default tables
        if WelcomeDialog.status == "New":
            M_OperateDatabases.create_study_tables(Study_Database)
            M_OperateDatabases.fillIndicatorsSetup(self.Methodology, self.Database)
            M_OperateDatabases.FillNewWeightsDatabase(self.Methodology, self.Database)
            
        else:
            self.update_situations_from_database()
            self.update_weights_from_database()
            self.update_indicators_from_database()

    def update_indicators_setup(self):
        self.IndicatorsSetup = M_OperateDatabases.fetch_table_from_database(self.Database, "IndicatorsSetup")
        self.IndicatorsSetup.set_index("IndicatorID", inplace=True)

    def add_labels_to_dataframes(self):
        '''
        ADD SOME COLUMNS TO DATAFRAMES FOR FURTHER PLOTING
        '''
        #Get the all the data from answers and tables and do some compatibilizations
        #Add ShortLabel and FullLabel to self.objectives
        self.objectives["ShortLabel"] = ''
        self.objectives["FullLabel"] = ''

        for index, row in self.objectives.iterrows():
            if row["DimensionID"] == 1:
                DimensionLetter = "F"
            elif row["DimensionID"] == 2:
                DimensionLetter = "P"
            self.objectives.at[index, "ShortLabel"] = f"Obj. {DimensionLetter}{row['ObjectiveSubID']}"
            self.objectives.at[index,"FullLabel"] = f"{self.objectives.at[index,'ShortLabel']} - {row['ObjectiveName']}"

        #Add ShortLabel and FullLabel to self.criteria
        self.criteria["ShortLabel"] = ''
        self.criteria["FullLabel"] = ''
        for index, row in self.criteria.iterrows():
            Dimension = row["ObjectiveID"].split(".")[0]
            Objective = row["ObjectiveID"].split(".")[1]
            if Dimension == "1":
                DimensionLetter = "F"
            elif Dimension == "2":
                DimensionLetter = "P"
            self.criteria.at[index,"ShortLabel"] = f"Crit. {DimensionLetter}{Objective}.{row['CriteriaSubID']}"
            self.criteria.at[index,"FullLabel"] = f"{self.criteria.at[index, 'ShortLabel']} - {row['CriteriaName']}"

    def set_files_and_paths(self, WelcomeDialog: WelcomeDialog):
        # Create a copy of the Methodology Database and Study Structure Database to the Study Directory
        Original_Methodology = 'database\REFUSS_V8.db'
        new_methodology_filename  = "RESILISTORM.db"

        Original_Study = 'database\Study_Structure.db'
        new_study_filename  = f"{self.Name}-STUDY.db"

        if WelcomeDialog.status == "New":
            # Make a copy of the Methodology Database to the Study Directory
            copy_and_rename_file(Original_Methodology, self.Directory, new_methodology_filename)

            # Make a copy of the Study Strucutre Database to the Study Directory
            copy_and_rename_file(Original_Study, self.Directory, new_study_filename)

        self.Methodology_path =  os.path.join(self.Directory, new_methodology_filename)
        self.Database_path = os.path.join(self.Directory, new_study_filename)       

    def update_situations_from_generator(self, SituationGenerator: M_SituationManager.SituationGenerator):
        for index, row in SituationGenerator.get_situations().iterrows():
            situation = C_RESILISTORM_Situation.Situation()
            situation.update_from_generator(SituationGenerator, row["SituationID"])
            self.Situations[situation.id] = situation

    def update_situations_from_database(self):
        situations = M_OperateDatabases.fetch_table_from_database(self.Database, "StudySituations")
        situations.set_index("SituationID", inplace=True)
        for situation_id, row in situations.iterrows():
            situation = C_RESILISTORM_Situation.SITUATION()
            situation.update_from_database(row)
            self.Situations[situation.id] = situation
   
    def update_weights_from_database(self):
        DimensionsWeight = M_OperateDatabases.fetch_table_from_database(self.Database, "DimensionsWeight")
        DimensionsWeight.set_index("DimensionID", inplace=True)
        ObjectivesWeight = M_OperateDatabases.fetch_table_from_database(self.Database, "ObjectivesWeight")
        ObjectivesWeight.set_index("ObjectiveID", inplace=True)
        CriteriaWeight = M_OperateDatabases.fetch_table_from_database(self.Database, "CriteriaWeight")
        CriteriaWeight.set_index("CriteriaID", inplace=True)
        self.Weights = {'Dimensions': DimensionsWeight, 'Objectives': ObjectivesWeight, 'Criteria': CriteriaWeight}
        
    def update_indicators_from_database(self):
        indicators_setup = M_OperateDatabases.fetch_table_from_database(self.Database, "IndicatorsSetup")
        self.Selected_indicators = indicators_setup[indicators_setup["SelectedState"] == 1].copy(deep = True)
        
        for index, row in self.Selected_indicators.iterrows():
            self.Selected_indicators.loc[index,  "IndicatorClass"] = re.sub(r'\d', '', row["IndicatorID"])
        
        self.Selected_indicators.set_index("IndicatorID", inplace = True)
        pass
    
def copy_and_rename_file(source_file, destination_directory, new_file_name):
    shutil.copy2(source_file, destination_directory)
    new_file_path = os.path.join(destination_directory, new_file_name)
    os.rename(os.path.join(destination_directory, os.path.basename(source_file)), new_file_path)

    return new_file_path