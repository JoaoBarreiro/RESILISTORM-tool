from PySide6.QtSql import QSqlDatabase, QSqlQuery

import pandas as pd
import os
import re
import shutil
from typing import Dict

from C_SITUATION import SITUATION
from M_WelcomeDialog import WelcomeDialog
import M_OperateDatabases
import M_ResilienceCalculus

class STUDY():

    def __init__(self,
                 WelcomeDialog: WelcomeDialog,
                 Methodolohy_Database: QSqlDatabase,
                 Study_Database: QSqlDatabase,
                 Temp_Database : QSqlDatabase
                 ):
        
        self.Name = WelcomeDialog.study_name
                
        self.Methodology_path: str = None
        self.Methodology_db = Methodolohy_Database
        
        self.Study_path = WelcomeDialog.study_directory
        self.Study_db = Study_Database
        
        self.Temp_db = Temp_Database
        
        self.dimension: pd.DataFrame = None
        self.objectives: pd.DataFrame = None
        self.criteria: pd.DataFrame = None
        self.metrics: pd.DataFrame = None
        self.metric_options: pd.DataFrame = None
        self.indicators: Dict[str, pd.DataFrame]  = {}
        
        self.Situations: Dict[int, SITUATION] = {}
        self.Selected_situation: SITUATION = None
        
        self.Weights: pd.DataFrame = None
        self.Selected_indicators: pd.DataFrame = None
        
        # Automatically initialize the methodology and database paths
        self.set_files_and_paths(WelcomeDialog)

        M_OperateDatabases.establishDatabaseConnections([(self.Methodology_db, self.Methodology_path),
                                                         (self.Study_db, self.Database_path)
                                                         ])

        refuss_contents = M_OperateDatabases.getREFUSSDatabase(self.Methodology_db)
        self.dimensions = refuss_contents[0]
        self.objectives = refuss_contents[1].set_index("ObjectiveID")
        self.criteria = refuss_contents[2].set_index("CriteriaID")
        self.metrics = refuss_contents[3].set_index("MetricID")
        self.metric_options = refuss_contents[4].set_index("MetricID")
        self.indicators = {'indicators_classes': refuss_contents[5].set_index("IndicatorClassID"),
                           'indicators_library': refuss_contents[6].set_index("IndicatorID")}
        
        #add short and full labels to dataframes
        self.add_labels_to_dataframes()        

        self.IndicatorsLibrary = M_OperateDatabases.fetch_table_from_database(self.Methodology_db, "IndicatorsLibrary")
        self.IndicatorsLibrary.set_index("IndicatorID", inplace=True)

        self.IndicatorsClassesLibrary = M_OperateDatabases.fetch_table_from_database(self.Methodology_db, "IndicatorsClassesLibrary")
        self.IndicatorsClassesLibrary.set_index("IndicatorClassID", inplace=True)             

        self.IndicatorsSetup = None

        # Create Study Database default tables
        if WelcomeDialog.status == "New":
            M_OperateDatabases.create_study_tables(Study_Database)
            M_OperateDatabases.fillIndicatorsSetup(self.Methodology_db, self.Study_db)
            M_OperateDatabases.FillNewWeightsDatabase(self.Methodology_db, self.Study_db)
            
        else:
            self.update_situations_from_database()
            self.update_weights_from_database()
            self.update_indicators_from_database()
  
    def update_study_from_AnalysisManager(self):
        self.update_situations_from_database()
        self.update_weights_from_database()
        self.update_indicators_from_database()

    def update_situation_from_SituationGenerator(self,
                          type: str,
                          situation_id: int):
        
        Situation = self.Situations[situation_id]
        # Set temporary connection to database ANSWERS_DB and apply needed changes
        M_OperateDatabases.establishDatabaseConnections([(self.Temp_db, Situation.db_path)])
        
        if type == "new":
            M_OperateDatabases.createSituationTables(self.Methodology_db, self.Study_db, self.Temp_db, Situation)
            M_OperateDatabases.fillMetricAnswersDatabase(self.Temp_db, self.metrics)
            self.Temp_db.close()
            print(f"File {Situation.id}-SITUATION.db created.")
            
        elif type == "update": 
            new_rows = set(Situation.rainfall)
                        
            tables = []
            query = QSqlQuery(self.Temp_db)
            query.exec('SELECT name FROM sqlite_master WHERE type="table"')
            while query.next():
                table_name = query.value(0)
                tables.append(table_name)
            
            for table in tables:
                if table == "B1":
                    existing_rows = set()
                    query.exec(f"SELECT DISTINCT RainfallID FROM B1")
                    while query.next():
                        existing_rows.add(int(query.value(0)))
                        
                    unchanged_rows= existing_rows.intersection(new_rows)
                        
                    rows_to_delete = existing_rows - unchanged_rows
                    for rain_id in rows_to_delete:
                        query.exec(f'DELETE FROM {table} WHERE RainfallID = {rain_id}')

                    rows_to_add = new_rows - unchanged_rows
                    
                    custom_building_uses = set()
                    query_study = QSqlQuery(self.Study_db)
                    query_study.exec('SELECT DISTINCT CustomUse FROM B1UsesSetup')
                    while query_study.next():
                        custom_building_uses.add(query_study.value(0))

                    for use in custom_building_uses:
                        query.exec(f"SELECT RainfallID FROM B1 WHERE BuildingUse = '{use}'")

                        for rain_id in rows_to_add:
                            query.exec(f"INSERT INTO B1 (RainfallID, BuildingUse) VALUES ({rain_id}, '{use}')")          

                elif table != ("B1" or "MetricAnswers"):
                    query.exec(f"SELECT RainfallID FROM {table}")
                    existing_rows = set()
                    while query.next():
                        existing_rows.add(int(query.value(0)))
                        
                    unchanged_rows= existing_rows.intersection(new_rows)
                    
                    rows_to_delete = existing_rows - unchanged_rows
                    for rain_id in rows_to_delete:
                        query.exec(f'DELETE FROM {table} WHERE RainfallID = {rain_id}')
                    
                    rows_to_add = new_rows - unchanged_rows
                    for rain_id in rows_to_add:
                        query.exec(f'INSERT INTO {table} VALUES ({rain_id})')
            print(f"File {situation_id}-SITUATION.db updated.")
            self.Temp_db.close()            
            
            self.update_situation_database_rainfalls(situation_id)
            
        elif type == "delete":
            self.Temp_db.close()
            if os.path.exists(Situation.db_path):
                os.remove(Situation.db_path)
                print(f"File {situation_id}-SITUATION.db deleted.")

    def update_situation_database_rainfalls(self,
                                            situation_id: int):
        
        Situation = self.Situations[situation_id]
        new_rows = set(Situation.rainfall)
        
        M_OperateDatabases.establishDatabaseConnections([(self.Temp_db, Situation.db_path)])
        
        tables = []
        query = QSqlQuery(self.Temp_db)
        query.exec('SELECT name FROM sqlite_master WHERE type="table"')
        while query.next():
            table_name = query.value(0)
            tables.append(table_name)
         
        for table in tables:
            if table == "B1":

                existing_rows = set()
                query.exec(f"SELECT DISTINCT RainfallID FROM B1")
                while query.next():
                    existing_rows.add(int(query.value(0)))
                    
                unchanged_rows= existing_rows.intersection(new_rows)
                    
                rows_to_delete = existing_rows - unchanged_rows
                for rain_id in rows_to_delete:
                    query.exec(f'DELETE FROM {table} WHERE RainfallID = {rain_id}')

                rows_to_add = new_rows - unchanged_rows
                
                custom_building_uses = set()
                query_study = QSqlQuery(self.Study_db)
                query_study.exec('SELECT DISTINCT CustomUse FROM B1UsesSetup')
                while query_study.next():
                    custom_building_uses.add(query_study.value(0))

                for use in custom_building_uses:
                    query.exec(f"SELECT RainfallID FROM B1 WHERE BuildingUse = '{use}'")

                    for rain_id in rows_to_add:
                        query.exec(f"INSERT INTO B1 (RainfallID, BuildingUse) VALUES ({rain_id}, '{use}')")          

            elif table != ("B1" and "MetricAnswers"):
                query.exec(f"SELECT RainfallID FROM {table}")
                existing_rows = set()
                while query.next():
                    existing_rows.add(int(query.value(0)))
                    
                unchanged_rows= existing_rows.intersection(new_rows)
                
                rows_to_delete = existing_rows - unchanged_rows
                for rain_id in rows_to_delete:
                    query.exec(f'DELETE FROM {table} WHERE RainfallID = {rain_id}')
                
                rows_to_add = new_rows - unchanged_rows
                for rain_id in rows_to_add:
                    query.exec(f'INSERT INTO {table} (RainfallID) VALUES ({rain_id})')
                    
        self.Temp_db.close()
    
    def update_indicators_setup(self):
        self.IndicatorsSetup = M_OperateDatabases.fetch_table_from_database(self.Study_db, "IndicatorsSetup")
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
        Original_Methodology = 'database\RESILISTORM_V0.db'
        new_methodology_filename  = "RESILISTORM.db"

        Original_Study = 'database\STUDY_Structure.db'
        new_study_filename  = f"{self.Name}-STUDY.db"

        if WelcomeDialog.status == "New":
            # Make a copy of the Methodology Database to the Study Directory
            copy_and_rename_file(Original_Methodology, self.Study_path, new_methodology_filename)

            # Make a copy of the Study Strucutre Database to the Study Directory
            copy_and_rename_file(Original_Study, self.Study_path, new_study_filename)

        self.Methodology_path =  os.path.join(self.Study_path, new_methodology_filename)
        self.Database_path = os.path.join(self.Study_path, new_study_filename)       

    def update_situations_from_database(self):
        situations_data = M_OperateDatabases.fetch_table_from_database(self.Study_db, "StudySituations")
        # situations_data.set_index("SituationID", inplace=True)
        for index, row in situations_data.iterrows():
            Situation = SITUATION(self.Study_path)
            Situation.update_from_table_row(row)
            self.Situations[Situation.id] = Situation
   
    def update_weights_from_database(self):
        DimensionsWeight = M_OperateDatabases.fetch_table_from_database(self.Study_db, "DimensionsWeight")
        DimensionsWeight.set_index("DimensionID", inplace=True)
        ObjectivesWeight = M_OperateDatabases.fetch_table_from_database(self.Study_db, "ObjectivesWeight")
        ObjectivesWeight.set_index("ObjectiveID", inplace=True)
        CriteriaWeight = M_OperateDatabases.fetch_table_from_database(self.Study_db, "CriteriaWeight")
        CriteriaWeight.set_index("CriteriaID", inplace=True)
        self.Weights = {'Dimensions': DimensionsWeight, 'Objectives': ObjectivesWeight, 'Criteria': CriteriaWeight}
        
    def update_indicators_from_database(self):
        indicators_setup = M_OperateDatabases.fetch_table_from_database(self.Study_db, "IndicatorsSetup")
        self.Selected_indicators = indicators_setup[indicators_setup["SelectedState"] == 1].copy(deep = True)
        
        for index, row in self.Selected_indicators.iterrows():
            self.Selected_indicators.loc[index,  "IndicatorClass"] = re.sub(r'\d', '', row["IndicatorID"])
        
        self.Selected_indicators.set_index("IndicatorID", inplace = True)
        pass

    def calculate_ratings(self):
        # Filter objectives and criteria from dimension 1
        functional_objectives = self.objectives[self.objectives["DimensionID"] == 1]
        functional_criteria = self.criteria[self.criteria.index.str.startswith("1.")]


        if self.Temp_db.isOpen():
            self.Temp_db.close()
            
        for Situation_id, Situation in self.Situations.items():
            # Set temporary connection to database ANSWERS_DB and apply needed changes
            M_OperateDatabases.establishDatabaseConnections([(self.Temp_db, Situation.db_path)])
            

            self.calculate_situation_functional_ratings(Situation, functional_objectives, functional_criteria)
            self.calculate_situation_performance_ratings(Situation)
            self.calculate_situation_overall_rating(Situation)
            self.Temp_db.close()
        

    def calculate_situation_functional_ratings(self,
                                               situation: SITUATION,
                                               functional_objectives: pd.DataFrame,
                                               functional_criteria: pd.DataFrame):
        
        if not situation.name: #Situation "none" is selected
            return
        
        # Get functional answers
        MetricsAnswers = M_OperateDatabases.fetch_table_from_database(self.Temp_db, "MetricAnswers")
        MetricsAnswers.set_index("metricID", inplace=True)
        situation.functional_answers = MetricsAnswers[MetricsAnswers.index.str.startswith('1.')]

        '''CALCULATE FUNCTIONAL COMPLETENESS'''
        # Calculate functional answers completeness
        functional_objectives_completeness = M_ResilienceCalculus.Calculate_Completeness(situation.functional_answers)
        # Merge the completeness dataframe with the functional objectives
        situation.functional_objectives_completeness = pd.merge(functional_objectives,
                                                                functional_objectives_completeness,
                                                                left_index = True, right_index =True , how='inner')
        
        '''CALCULATE FUNCTIONAL RATINGS'''
        functional_dimension_rating, functional_objectives_rating, functional_criteria_rating = M_ResilienceCalculus.Calculate_FunctionalRating(self.Weights,
                                                                                                                                            self.metrics,
                                                                                                                                            self.metric_options,
                                                                                                                                            situation.functional_answers)
        
        situation.functional_objectives_rating = functional_objectives_rating.join(functional_objectives[["ObjectiveName", "ShortLabel", "FullLabel"]].loc[functional_objectives.index], how = "right")
        situation.functional_criteria_rating = functional_criteria_rating.join(functional_criteria[["CriteriaName", "ShortLabel", "FullLabel"]].loc[functional_criteria.index], how = "right")
        situation.functional_rating = functional_dimension_rating.at["1", "Rating"]

    def calculate_situation_performance_ratings(self, situation: SITUATION):
        if not situation.name: #Situation "none" is selected
            return
        
        '''CALCULATE SYSTEM PERFORMANCE RATING'''
        situation.system_performance_rating = M_ResilienceCalculus.Calculate_SystemPerformanceRating(AnswersDatabase = self.Temp_db,
                                                                                                        IndicatorsLibrary = self.IndicatorsLibrary,
                                                                                                        IndicatorsSetup = self.IndicatorsSetup,
                                                                                                        Situation = situation)
        
        situation.system_performance_final_rating = M_ResilienceCalculus.Calculate_Integral(situation.system_performance_rating)
        
        '''CALCULATE SYSTEM CONSEQUENCES RATING'''
        situation.system_consequences_rating = M_ResilienceCalculus.Caculate_ConsequencesRating(StudyDatabase = self.Study_db,
                                                                                            AnswersDatabase = self.Temp_db,
                                                                                            IndicatorsLibrary = self.IndicatorsLibrary,
                                                                                            IndicatorsSetup = self.IndicatorsSetup,
                                                                                            Situation = situation)            
        
        situation.system_consequences_final_rating = M_ResilienceCalculus.Calculate_Integral(situation.system_consequences_rating)
        
        '''CALCULATE PERFORMANCE DIMENTSION RATING'''
        situation.performance_rating = M_ResilienceCalculus.Caculate_PerformanceDimensionRating(self.Weights,
                                                                                                situation.system_performance_final_rating,
                                                                                                situation.system_consequences_final_rating)
        
    def calculate_situation_overall_rating(self, situation: SITUATION):
        if not situation.name: #Situation "none" is selected
            return
        
        situation.overall_rating = M_ResilienceCalculus.Caculate_OverallDimensionRating(self.Weights,
                                                                                        situation.functional_rating,
                                                                                        situation.performance_rating)

def copy_and_rename_file(source_file, destination_directory, new_file_name):
    shutil.copy2(source_file, destination_directory)
    new_file_path = os.path.join(destination_directory, new_file_name)
    os.rename(os.path.join(destination_directory, os.path.basename(source_file)), new_file_path)

    return new_file_path
