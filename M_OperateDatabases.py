from os import path
import pandas as pd
import sys
from PySide6.QtSql import QSqlQuery, QSqlDatabase

import M_SituationManager

def establishDatabaseConnections(DatabaseList: list):
    """
    Establishes database connections.

    Parameters:
        DatabaseList: a list of tuples containing the database and its path.

    """

    for set in DatabaseList:
        database = set[0]
        path = set[1]
        
        database.setDatabaseName(path)
        if not database.open():
            print(f"Error: Failed to open {path}")

def closeDatabaseConnections(DatabaseList: list):
    """
    Close database connections.

    Args:
        DatabaseList (list): List of database objects.
    """
    for database in DatabaseList:
        if database.isOpen():
            database.close()

def createSituationTables(REFUSS_Database:QSqlDatabase, Study_database: QSqlDatabase, Situation_Database: QSqlDatabase, Situation: M_SituationManager.Situation):
    
    query = QSqlQuery(Situation_Database)

    '''Set Functional Metrics answer table'''
    
    if query.exec("CREATE TABLE IF NOT EXISTS MetricAnswers ("
               "criteriaID TEXT, "
               "metricID TEXT PRIMARY KEY, "
               "answer TEXT, "
               "comment TEXT)"
               ):
        Situation_Database.commit()
    else:
        print(f"Error creating MetricAnswers table: {query.lastError().text()}")
    
    ''' Set Performance Metrics answer tables '''
    
    # Create Performance Metrics answers tables
    IndicatorsLibrary = fetch_table_from_database(REFUSS_Database, "IndicatorsLibrary")
    IndicatorsLibrary.set_index("IndicatorID", inplace = True)
            
    Indicators_tables = Situation_Database.tables()
    
    for indicatorID, properties in IndicatorsLibrary.iterrows():
        ClassesLabels = properties["ClassesLabel"].split("; ")
        
        # Generate the SQL query to create the table with dynamic column names
        columns = []
        for index, label in enumerate(ClassesLabels):
            columns.append(f"[{label}] REAL")
        
        columns_str = ", ".join(columns)
        
        if indicatorID not in Indicators_tables:
            if indicatorID == 'B1':
                rainfall_column = "RainfallID INTEGER ," #NOT UNIQUE!
                extra_column = f"BuildingUse TEXT , "
            else:
                rainfall_column = "RainfallID INTEGER UNIQUE ," 
                extra_column = ""
            
            if query.exec(f"CREATE TABLE {indicatorID} ({rainfall_column} {extra_column} {columns_str});"):
                Situation_Database.commit()
                
                if indicatorID == 'B1':               
                    updateB1TableUses(Situation_Database, Study_database, Situation)
                else:
                    # Create a different variable for the inner loop
                    rainfall_values = Situation.rainfall
                    for rainfall_id in rainfall_values:
                        if query.exec(f"INSERT INTO {indicatorID} (RainfallID) VALUES ('{rainfall_id}');"):
                            Situation_Database.commit()
                        else:
                            print(f"Error inserting RainfallID {rainfall_id} into {indicatorID}: {query.lastError().text()}")
            else:
                print(f"Error creating {indicatorID} table in setConsequencesTables: {query.lastError().text()} in setConsequencesTables")
    return

'''    # if not query.exec("CREATE TABLE IF NOT EXISTS ScenarioSetup ("
    #            "RainfallID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,"
    #            "ScenarioName TEXT UNIQUE, "
    #            "ScenarioSystemConfig TEXT, "
    #            "ScenarioRainfall TEXT, "
    #            "ScenarioOutfall TEXT, "
    #            "ScenarioComment TEXT)"
    #            ):
    #     print(f"Error creating ScenarioSetup table: {query.lastError().text()}")

    # if not query.exec("CREATE TABLE IF NOT EXISTS HazardSetup ("
    #            "HazardName TEXT PRIMARY KEY, "
    #            "HazardUnit TEXT, "
    #            "HazardComment TEXT)"
    #            ):
    #     print(f"Error creating HazardSetup table: {query.lastError().text()}")
        
    # if not query.exec("CREATE TABLE IF NOT EXISTS IndicatorsSetup ("
    #            "IndicatorID TEXT UNIQUE, "
    #            "SelectedUnit TEXT, "
    #            "IndicatorComplement TEXT, "
    #            "SelectedState INTEGER )"
    #            ):
    #     print(f"Error creating IndicatorsSetup table: {query.lastError().text()}")

    # if not query.exec("CREATE TABLE IF NOT EXISTS PerformanceAnswers ("
    #            "ScenarioID INTEGER PRIMARY KEY, "
    #            "M2111 TEXT, "
    #            "M2112 TEXT, "
    #            "M2121 TEXT, "
    #            "FOREIGN KEY (ScenarioID) REFERENCES ScenarioSetup (ScenarioID) ON DELETE CASCADE ON UPDATE CASCADE)"
    #            ):
    #     print(f"Error creating PerformanceAnswers table: {query.lastError().text()}")

    # if not query.exec("CREATE TABLE IF NOT EXISTS HazardAnswers ("
    #         "HazardName TEXT, "
    #         "ScenarioID INTEGER, "
    #         "FOREIGN KEY (HazardName) REFERENCES HazardSetup (HazardName) ON DELETE CASCADE ON UPDATE CASCADE,"
    #         "FOREIGN KEY (ScenarioID) REFERENCES ScenarioSetup (ScenarioID) ON DELETE CASCADE ON UPDATE CASCADE)"
    #         ):
    #     print(f"Error creating HazardAnswers table: {query.lastError().text()}")

    # for i in range(1, 11):
    #     query.exec(f"ALTER TABLE HazardAnswers ADD COLUMN Class{i} TEXT")
    
    ######### QUERIES TO UPDATE TABLES ##################

    # query.exec("DROP TRIGGER IF EXISTS Upload_ScenarioID_at_PerformanceAnswers")
    # if not query.exec("""
    #     CREATE TRIGGER Upload_ScenarioID_at_PerformanceAnswers
    #     AFTER INSERT ON ScenarioSetup
    #     FOR EACH ROW
    #     BEGIN
    #         INSERT INTO PerformanceAnswers (ScenarioID) VALUES (NEW.ScenarioID);
    #     END
    # """):
    #     print(f"Error Upload_ScenarioID_at_PerformanceAnswers: {query.lastError().text()}")

    # query.exec("DROP TRIGGER IF EXISTS Update_ScenarioID")
    # if not query.exec("""
    #     CREATE TRIGGER Update_ScenarioID
    #     AFTER UPDATE OF ScenarioID ON ScenarioSetup
    #     FOR EACH ROW
    #     BEGIN
    #         UPDATE PerformanceAnswers
    #         SET ScenarioID = NEW.ScenarioID
    #         WHERE ScenarioID = OLD.ScenarioID;

    #         UPDATE HazardAnswers
    #         SET ScenarioID = NEW.ScenarioID
    #         WHERE ScenarioID = OLD.ScenarioID;
    #     END
    # """):
    #     print(f"Error Update_ScenarioID: {query.lastError().text()}")

    # query.exec("DROP TRIGGER IF EXISTS Update_HazardName")
    # if not query.exec("""
    #     CREATE TRIGGER Update_HazardName
    #     AFTER UPDATE OF HazardName ON HazardSetup
    #     FOR EACH ROW
    #     BEGIN
    #         UPDATE HazardAnswers
    #         SET HazardName = NEW.HazardName
    #         WHERE HazardName = OLD.HazardName;
    #     END
    # """):
    #     print(f"Error Update_ScenarioID: {query.lastError().text()}")

    # query.exec("DROP TRIGGER IF EXISTS Delete_Scenario")
    # if not query.exec("""
    #     CREATE TRIGGER Delete_Scenario
    #     AFTER DELETE ON ScenarioSetup
    #     FOR EACH ROW
    #     BEGIN
    #         DELETE FROM PerformanceAnswers
    #         WHERE ScenarioID = OLD.ScenarioID;

    #         DELETE FROM HazardAnswers
    #         WHERE ScenarioID = OLD.ScenarioID;
    #     END
    # """):
    #     print(f"Error Delete_Scenario: {query.lastError().text()}")

    # query.exec("DROP TRIGGER IF EXISTS INSERT INTODelete_Hazard")
    # if not query.exec("""
    #     CREATE TRIGGER IF NOT EXISTS Delete_Hazard
    #     AFTER DELETE ON HazardSetup
    #     BEGIN
    #         DELETE FROM HazardAnswers
    #         WHERE HazardName = OLD.HazardName;
    #     END;
    # """):
    #     print(f"Error Delete_Hazard: {query.lastError().text()}")


    ######### QUERIES FOR HAZARD ANSWERS TABLE UPDATE ##################

    # query.exec("DROP TRIGGER IF EXISTS Insert_HazardAnswers_from_HazardSetup")
    # if not query.exec("""
    #     CREATE TRIGGER IF NOT EXISTS Insert_HazardAnswers_from_HazardSetup
    #     AFTER INSERT ON HazardSetup
    #     BEGIN
    #         INSERT INTO HazardAnswers (HazardName, ScenarioID)
    #             SELECT NEW.HazardName, ScenarioID
    #             FROM ScenarioSetup;
    #     END;
    # """):
    #     print(f"Error Insert_HazardAnswers_from_HazardSetup: {query.lastError().text()}")

    # query.exec("DROP TRIGGER IF EXISTS Insert_HazardAnswers_from_ScenarioSetup")
    # if not query.exec("""
    #     CREATE TRIGGER IF NOT EXISTS Insert_HazardAnswers_from_ScenarioSetup
    #     AFTER INSERT ON ScenarioSetup
    #     BEGIN
    #         INSERT INTO HazardAnswers (HazardName, ScenarioID)
    #             SELECT HazardName, NEW.ScenarioID
    #             FROM HazardSetup;
    #     END;
    # """):
    #     print(f"Error Insert_HazardAnswers_from_ScenarioSetup: {query.lastError().text()}")'''

def create_study_tables(Study_Database: QSqlDatabase):
    
    query = QSqlQuery(Study_Database)

    if not query.exec("CREATE TABLE IF NOT EXISTS IndicatorsSetup ("
               "IndicatorID TEXT UNIQUE, "
               "SelectedUnit TEXT, "
               "IndicatorComplement TEXT, "
               "SelectedState INTEGER )"
               ):
        print(f"Error creating IndicatorsSetup table: {query.lastError().text()}")
    
    if not query.exec("CREATE TABLE IF NOT EXISTS DimensionsWeight ("
               "DimensionID TEXT UNIQUE, "
               "DimensionName TEXT,"
               "Weight REAL)"
               ):
        print(f"Error creating DimensionsWeight table: {query.lastError().text()}")

    if not query.exec("CREATE TABLE IF NOT EXISTS ObjectivesWeight ("
               "ObjectiveID TEXT UNIQUE, "
               "ObjectiveName TEXT,"
               "Weight REAL)"
               ):
        print(f"Error creating ObjectivesWeight table: {query.lastError().text()}")

    if not query.exec("CREATE TABLE IF NOT EXISTS CriteriaWeight ("
               "CriteriaID TEXT UNIQUE, "
               "CriteriaName TEXT,"
               "Weight REAL)"
               ):
        print(f"Error creating CriteriaWeight table: {query.lastError().text()}")

    """criar tabela na database se não existir B1UsesSetup"""
    if not query.exec("CREATE TABLE IF NOT EXISTS B1UsesSetup ("
                "CustomUse TEXT, "
                "TotalSize NUMERIC, "
                "MethodologyClass TEXT)"
            ):
            print(f"Failed to create table B1Settings. {query.lastError().text()}")

def FillNewWeightsDatabase(REFUSS_Database: QSqlDatabase, Target_Database: QSqlDatabase):

    # Create the Dimensions_Weight table
    query_A = QSqlQuery(REFUSS_Database)
    query_B = QSqlQuery(Target_Database)
    
    # Retrieve the dimensions from the Dimensions table
    query_A.exec('SELECT DimensionID, DimensionName FROM Dimensions;')
    
    dimensions = {}
    while query_A.next():
        dimension_id = query_A.value(0)
        dimension_name = query_A.value(1)
        dimensions[dimension_id] = dimension_name

    for dimension_id, dimension_name in dimensions.items():
        # Calculate and populate the weights for Dimensions_Weight table
        dimension_weight = 1 / len(dimensions)

        if query_B.exec(f"INSERT INTO DimensionsWeight VALUES ('{dimension_id}', '{dimension_name}', '{dimension_weight}');"):
            Target_Database.commit()
        else:
            print(f"Error inserting into DimensionsWeight: {query_B.lastError().text()}")
        # query_B.addBindValue(dimension_id)
        # query_B.addBindValue(dimension_name)
        # query_B.addBindValue(dimension_weight)
        # query_B.exec()

        # Retrieve the objectives within the current dimension
        query_A.exec(f"SELECT ObjectiveID, ObjectiveName FROM Objectives WHERE DimensionID = '{dimension_id}';")
            # query_A.addBindValue(dimension_id)
            # query_A.exec()
        objectives = {}
        while query_A.next():
            objective_id = query_A.value(0)
            objective_name = query_A.value(1)
            objectives[objective_id] = objective_name

        for objective_id, objective_name in objectives.items():
            # Calculate and populate the weights for Objectives_Weight table within the current dimension
            objective_weight = 1 / len(objectives)

            if query_B.exec(f"INSERT INTO ObjectivesWeight VALUES ('{objective_id}', '{objective_name}', '{objective_weight}');"):
                Target_Database.commit()
            else:
                print(f"Error inserting into ObjectivesWeight: {query_B.lastError().text()}")
            
            # query_B.prepare('INSERT INTO ObjectivesWeight VALUES (?, ?, ?)')
            # query_B.addBindValue(objective_id)
            # query_B.addBindValue(objective_name)
            # query_B.addBindValue(objective_weight)
            # query_B.exec()

            # Retrieve the criteria within the current objective
            # query_A.prepare('SELECT CriteriaID, CriteriaName FROM Criteria WHERE ObjectiveID = ?')
            # query_A.addBindValue(objective_id)
            # query_A.exec()
            
            criteria = {}
            query_A.exec(f"SELECT CriteriaID, CriteriaName FROM Criteria WHERE ObjectiveID = '{objective_id}';")
            while query_A.next():
                criteria_id = query_A.value(0)
                criteira_name = query_A.value(1)
                criteria[criteria_id] = criteira_name

            for criteria_id, criteria_name in criteria.items():
                # Calculate and populate the weights for Criteria_Weight table within the current objective
                criteria_weight = 1 / len(criteria)

                if query_B.exec(f"INSERT INTO CriteriaWeight VALUES ('{criteria_id}', '{criteria_name}', '{criteria_weight}');"):
                    Target_Database.commit()
                else:
                    print(f"Error inserting into CriteriaWeight: {query_B.lastError().text()}")
                # query_B.prepare('INSERT INTO CriteriaWeight VALUES (?, ?, ?)')
                # query_B.addBindValue(criteria_id)
                # query_B.addBindValue(criteria_name)
                # query_B.addBindValue(criteria_weight)
                # query_B.exec()

def fillIndicatorsSetup(REFUSS_Database: QSqlDatabase, Target_Database: QSqlDatabase):
    # Connect to both databases
    if REFUSS_Database.isOpen() and Target_Database.isOpen():
        refuss_query = QSqlQuery(REFUSS_Database)
        answers_query = QSqlQuery(Target_Database)

        # Retrieve unique 'IndicatorID' values from the REFUSS_Database table
        refuss_query.exec("SELECT IndicatorID FROM IndicatorsLibrary")

        # Iterate through the retrieved 'IndicatorID' values and insert them into Answers_Database
        while refuss_query.next():
            indicator_id = refuss_query.value(0)

            # Insert 'IndicatorID' into Answers_Database table
            insert_query = f"INSERT INTO IndicatorsSetup (IndicatorID, SelectedState) VALUES ('{indicator_id}', 0)"
            if answers_query.exec(insert_query):
                print(f"Inserted {indicator_id} into Answers_Database")
            else:
                print(f"Failed to insert {indicator_id} into Answers_Database")

        # Commit the changes to the Answers_Database
        Target_Database.commit()
    else:
        print("Both databases must be open before running this function")    


"""def setConsequencesTables(REFUSS_Database: QSqlDatabase, Answers_Database: QSqlDatabase, Situation: M_AnalysisManager.Situation):
  
    '''Criar as restantes tabelas'''
    IndicatorsLibrary = fetch_table_from_database(REFUSS_Database, "IndicatorsLibrary")
    IndicatorsLibrary.set_index("IndicatorID", inplace = True)
        
    query = QSqlQuery(Answers_Database)
    
    Indicators_tables = Answers_Database.tables()
    for indicatorID, properties in IndicatorsLibrary.iterrows():
        ClassesLabels = properties["ClassesLabel"].split("; ")
        
        # Generate the SQL query to create the table with dynamic column names
        columns = []
        for index, label in enumerate(ClassesLabels):
            columns.append(f"[{label}] REAL")
        
        columns_str = ", ".join(columns)
        
        if indicatorID not in Indicators_tables:
            if indicatorID == 'B1':
                rainfall_column = f"RainfallID INTEGER UNIQUE"
                extra_column = f"BuildingUse TEXT , "
            else:
                rainfall_column = "RainfallID INTEGER UNIQUE"
                extra_column = ""
            if query.exec(f"CREATE TABLE {indicatorID} ("
                    f"{rainfall_column}"
                    f"{extra_column}"
                    f"{columns_str})"
                    ):

                if indicatorID == 'B1':
                    updateB1TableUses(Answers_Database)
                else:
                    # Create a different variable for the inner loop
                    inner_query = QSqlQuery(Answers_Database)
                    rainfall_values = Situation.rainfall
                    for rainfall_id in rainfall_values:
                        if not inner_query.exec(f"INSERT INTO {indicatorID} (RainfallID) VALUES ('{rainfall_id}')"):
                            print(f"Error inserting RainfallID {rainfall_id} into {indicatorID}: {query.lastError().text()}")
            else:
                print(f"Error creating {indicatorID} table in setConsequencesTables: {query.lastError().text()} in setConsequencesTables")
"""

"""def setB1Table(Situation_Database: QSqlDatabase, Situation: M_AnalysisManager.Situation):
    if not Situation_Database.isValid() or not Situation_Database.isOpen():
        return

    query = QSqlQuery(Situation_Database)
    
    custom_uses = []
    query.exec("SELECT DISTINCT customUse FROM B1UsesSetup")
    while query.next():
        use = query.value(0)
        custom_uses.append(use)
                
    # Get the list of unique RainfallID values from the B1 table
    scenario_ids = []
    query.exec("SELECT DISTINCT RainfallID FROM ScenarioSetup")
    while query.next():
        scenario_id = query.value(0)
        scenario_ids.append(scenario_id)

    # Check if the CustomUse already exists in the B1 table and insert if not
    for scenario_id in scenario_ids:
        for custom_use in custom_uses:
            query.exec(
                f"
                SELECT BuildingUse FROM B1
                WHERE RainfallID = {scenario_id} AND BuildingUse = '{custom_use}'
                "
            )

            # If not found, insert a new row
            if not query.next():
                query.exec(
                    f"INSERT INTO B1 (RainfallID, BuildingUse) VALUES ({scenario_id}, '{custom_use}')"
                    )
                # Handle any errors that might occur
                if not query.isActive():
                    print(f"Error inserting data: {query.lastError().text()}")

    # Remove CustomUse entries from the B1 table if they were removed
    for scenario_id in scenario_ids:
        query.exec(
            f"
            DELETE FROM B1
            WHERE RainfallID = {scenario_id} AND BuildingUse NOT IN ({", ".join(["'" + custom_use + "'" for custom_use in custom_uses])})
            "
        )
        # Handle any errors that might occur
        if not query.isActive():
            print(f"Error deleting data: {query.lastError().text()}")

    # Commit the changes to the database
    if not Situation_Database.commit():
        print(f"Error committing changes in setB1Table: {query.lastError().text()}")
"""

def updateB1TableUses(Situation_Database: QSqlDatabase,
                  Study_Database: QSqlDatabase,
                  Situation: M_SituationManager.Situation,
                  old_value: str = None,
                  new_value: str = None):
    
    if not Situation_Database.isValid() or not Situation_Database.isOpen():
        return
    
    updated_custom_uses = []
    query_updated_uses = QSqlQuery(Study_Database)
    query_updated_uses.exec("SELECT DISTINCT CustomUse FROM B1UsesSetup")
    while query_updated_uses.next():
        use = query_updated_uses.value(0)
        updated_custom_uses.append(use)

    rainfalls = Situation.rainfall

    query_situation = QSqlQuery(Situation_Database)

    if not old_value and new_value:         # Insert new building use value
        for rain in rainfalls:
            if query_situation.exec(f"INSERT INTO B1 (RainfallID, BuildingUse) VALUES ({rain}, '{new_value}');"):
                Situation_Database.commit()
            else:
                print(f"Error inserting data in updateB1TableUses: {query_situation.lastError().text()}") 
    elif old_value and not new_value:       # Delete old value
        if query_situation.exec(f"DELETE FROM B1 WHERE BuildingUse = '{old_value}';"):
            Situation_Database.commit()
        else:
            print(f"Error deleting data in updateB1TableUses: {query_situation.lastError().text()}")
    elif old_value and new_value:           # Update the old value with the new value -> data changed
        for custom_use in updated_custom_uses:
            if custom_use == new_value:  
                if query_situation.exec(f"UPDATE B1 SET BuildingUse = '{new_value}' WHERE BuildingUse = '{old_value}';"):
                    Situation_Database.commit()
                else:
                    print(f"Error updating data in updateB1TableUses: {query_situation.lastError().text()}")
    elif not old_value and not new_value:   # in the case of creating the table (1st time call)
        for rain in rainfalls:
            for custom_use in updated_custom_uses:
                    if query_situation.exec(f"INSERT INTO B1 (RainfallID, BuildingUse) VALUES ({rain}, '{custom_use}');"):
                        Situation_Database.commit()
 
def getREFUSSDatabase(REFUSS_Database: QSqlDatabase):

    query = QSqlQuery(REFUSS_Database)

    dimension_query = ("SELECT * FROM Dimensions", "Dimensions")
    objectives_query = ("SELECT * FROM Objectives", "Objectives")
    criteria_query = ("SELECT * FROM Criteria", "Criteria")
    metrics_query = ("SELECT * FROM Metrics", "Metrics")
    metrics_options_query = ("SELECT * FROM MetricsOptions", "MetricsOptions")
    indicators_classes_query = ("SELECT * FROM IndicatorsClassesLibrary", "IndicatorsClasses")
    indicators_library_query = ("SELECT * FROM IndicatorsLibrary", "IndicatorsLibrary")

    all_queries = [dimension_query,
                    objectives_query,
                    criteria_query,
                    metrics_query,
                    metrics_options_query,
                    indicators_classes_query,
                    indicators_library_query]

    Results = []

    for option in all_queries:
        query.prepare(option[0])
        if query.exec():
            column_names = [query.record().fieldName(i) for i in range(query.record().count())]
            df = pd.DataFrame(columns=column_names)
            while query.next():
                row_data = [query.value(i) for i in range(query.record().count())]
                df.loc[len(df)] = row_data
            Results.append(df)
        else:
            error_message = query.lastError().text()
            print(f"Query execution failed: {error_message}")
            Results.append(None)

    return Results

def ObjectivesFromDimension(REFUSS_Database: QSqlDatabase, dimension_id: int):
    
    query = QSqlQuery(REFUSS_Database)
    query.exec(f"SELECT ObjectiveID, ObjectiveSubID, ObjectiveName FROM Objectives WHERE DimensionID = '{dimension_id}';")
    # query.addBindValue(dimension_id)
    # query.exec()

    objectives = []
    while query.next():
        objective_id = query.value(0)
        objective_subid = query.value(1)
        objective_name = query.value(2)
        objectives.append((objective_id, objective_subid, objective_name))
    return objectives

def CriteriaFromDimension(REFUSS_Database: QSqlDatabase, dimension_id: int):
    query = QSqlQuery(REFUSS_Database)
    query.prepare("""
        SELECT Objectives.ObjectiveID, Criteria.CriteriaID, Criteria.CriteriaSubID, Criteria.CriteriaName
        FROM Objectives
        JOIN Criteria ON Objectives.ObjectiveID = Criteria.ObjectiveID
        WHERE Objectives.DimensionID = ?
    """)
    query.addBindValue(dimension_id)
    query.exec()
    criteria = []
    while query.next():
        objective_id = query.value(0)
        criteria_id = query.value(1)
        criteria_subid = query.value(2)
        criteria_name = query.value(3)
        criteria.append((objective_id, criteria_id, criteria_subid, criteria_name))

    return criteria

def fillMetricAnswersDatabase(AnswersDatabase: QSqlDatabase, metrics: pd.DataFrame):

    # Clean existing contents of the answers table
    # tables = AnswersDatabase.tables()
    # query = QSqlQuery(AnswersDatabase)
    # for table in tables:
    #     query.exec(f"DELETE FROM {table}")

    # query.clear()
    
    MetricsID = metrics.index.to_list()
    CriteriaID = metrics["CriteriaID"]
    
    query = QSqlQuery(AnswersDatabase)

    for metric, criteria in zip(MetricsID, CriteriaID):
        if query.exec(f"INSERT INTO MetricAnswers (criteriaID, metricID) VALUES ('{criteria}', '{metric}')"):
            AnswersDatabase.commit()        
        # query.bindValue(":value1", criteria)
        # query.bindValue(":value2", metric)
        # query.exec()

def save_answer_to_AnswersDatabase(AnswersDatabase: QSqlDatabase, metricID: str, new_answer: str, newcomment: str):
    query = QSqlQuery(AnswersDatabase)
    query.prepare("UPDATE MetricAnswers SET answer = :answer, comment = :comment WHERE metricID = :metricID")
    query.bindValue(":metricID", metricID)
    query.bindValue(":answer", new_answer)
    query.bindValue(":comment", newcomment)
    query.exec()

def save_comment_to_AnswersDatabase(AnswersDatabase: QSqlDatabase, metricID: str, newcomment: str):
    query = QSqlQuery(AnswersDatabase)
    query.prepare("UPDATE MetricAnswers SET comment = :comment WHERE metricID = :metricID")
    query.bindValue(":metricID", metricID)
    query.bindValue(":comment", newcomment)
    query.exec()
    
def fetch_table_from_database(Database, TableName):
    if not Database.isOpen():
        print(f"Failed to connect to the database {Database} to fetch table {TableName}.")
        sys.exit()

    query = QSqlQuery(Database)
    query.exec(f"SELECT * FROM {TableName}")

    # Create a pandas DataFrame to store the fetched data
    columns = []
    rows = []
    record = query.record()
    for i in range(record.count()):
        columns.append(record.fieldName(i))
    while query.next():
        row = [query.value(i) for i in range(record.count())]
        rows.append(row)
    df = pd.DataFrame(rows, columns=columns)

    return df

def countDatabaseRows(Database: QSqlDatabase, TableName: str):
    """
    Counts the number of rows in a database table.

    Parameters:
    - Database (QSqlDatabase): The database connection to use for the query.
    - TableName (str): The name of the table to count the rows from.

    Returns:
    - row_count (int): The total number of rows in the specified table.
    - bool: False if the query execution fails or if the row count retrieval fails.
    """ 
    
    query = QSqlQuery(Database)
    query.prepare(f"SELECT COUNT(*) FROM {TableName}")
    if query.exec():
        if query.next():
            row_count = query.value(0)
        return row_count
    return False

def getUniqueColumnValues(Database: QSqlDatabase, TableName: str, ColumnName: str):
    """
    Retrieves a list of unique values from a specific column in a database table.

    Parameters:
    - Database (QSqlDatabase): The database connection to use for the query.
    - TableName (str): The name of the table to retrieve values from.
    - ColumnName (str): The name of the column from which to fetch unique values.

    Returns:
    - unique_values (list): A list of unique values from the specified column.
    - bool: False if the query execution fails.
    """

    query = QSqlQuery(Database)
    query.prepare(f"SELECT DISTINCT {ColumnName} FROM {TableName}")

    if query.exec():
        unique_values = []
        while query.next():
            value = query.value(0)
            unique_values.append(value) if value not in unique_values else None
        return unique_values
    return False