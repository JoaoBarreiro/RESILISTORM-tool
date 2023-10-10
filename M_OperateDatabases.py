from os import path
import pandas as pd
import sys
from PySide6.QtSql import QSqlQuery, QSqlDatabase

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

def verifyAnswersDatabase(Answers_Database: QSqlDatabase):
    
    query = QSqlQuery(Answers_Database)

    ######### QUERIES TO CREATE TABLES ##################

    if not query.exec("CREATE TABLE IF NOT EXISTS MetricAnswers ("
               "criteriaID TEXT, "
               "metricID TEXT PRIMARY KEY, "
               "answer TEXT, "
               "comment TEXT)"
               ):
        print(f"Error creating MetricAnswers table: {query.lastError().text()}")

    if not query.exec("CREATE TABLE IF NOT EXISTS ScenarioSetup ("
               "ScenarioID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,"
               "ScenarioName TEXT UNIQUE, "
               "ScenarioSystemConfig TEXT, "
               "ScenarioRainfall TEXT, "
               "ScenarioOutfall TEXT, "
               "ScenarioComment TEXT)"
               ):
        print(f"Error creating ScenarioSetup table: {query.lastError().text()}")

    if not query.exec("CREATE TABLE IF NOT EXISTS HazardSetup ("
               "HazardName TEXT PRIMARY KEY, "
               "HazardUnit TEXT, "
               "HazardComment TEXT)"
               ):
        print(f"Error creating HazardSetup table: {query.lastError().text()}")
        
    if not query.exec("CREATE TABLE IF NOT EXISTS IndicatorsSetup ("
               "IndicatorID TEXT UNIQUE, "
               "IndicatorUnit TEXT, "
               "IndicatorComplement TEXT)"
               ):
        print(f"Error creating IndicatorsSetup table: {query.lastError().text()}")

    if not query.exec("CREATE TABLE IF NOT EXISTS PerformanceAnswers ("
               "ScenarioID INTEGER PRIMARY KEY, "
               "M2111 TEXT, "
               "M2112 TEXT, "
               "M2121 TEXT, "
               "FOREIGN KEY (ScenarioID) REFERENCES ScenarioSetup (ScenarioID) ON DELETE CASCADE ON UPDATE CASCADE)"
               ):
        print(f"Error creating PerformanceAnswers table: {query.lastError().text()}")

    if not query.exec("CREATE TABLE IF NOT EXISTS HazardAnswers ("
            "HazardName TEXT, "
            "ScenarioID INTEGER, "
            "FOREIGN KEY (HazardName) REFERENCES HazardSetup (HazardName) ON DELETE CASCADE ON UPDATE CASCADE,"
            "FOREIGN KEY (ScenarioID) REFERENCES ScenarioSetup (ScenarioID) ON DELETE CASCADE ON UPDATE CASCADE)"
            ):
        print(f"Error creating HazardAnswers table: {query.lastError().text()}")

    for i in range(1, 11):
        query.exec(f"ALTER TABLE HazardAnswers ADD COLUMN Class{i} TEXT")


    ######### QUERIES TO UPDATE TABLES ##################

    query.exec("DROP TRIGGER IF EXISTS Upload_ScenarioID_at_PerformanceAnswers")
    if not query.exec("""
        CREATE TRIGGER Upload_ScenarioID_at_PerformanceAnswers
        AFTER INSERT ON ScenarioSetup
        FOR EACH ROW
        BEGIN
            INSERT INTO PerformanceAnswers (ScenarioID) VALUES (NEW.ScenarioID);
        END
    """):
        print(f"Error Upload_ScenarioID_at_PerformanceAnswers: {query.lastError().text()}")

    query.exec("DROP TRIGGER IF EXISTS Update_ScenarioID")
    if not query.exec("""
        CREATE TRIGGER Update_ScenarioID
        AFTER UPDATE OF ScenarioID ON ScenarioSetup
        FOR EACH ROW
        BEGIN
            UPDATE PerformanceAnswers
            SET ScenarioID = NEW.ScenarioID
            WHERE ScenarioID = OLD.ScenarioID;

            UPDATE HazardAnswers
            SET ScenarioID = NEW.ScenarioID
            WHERE ScenarioID = OLD.ScenarioID;
        END
    """):
        print(f"Error Update_ScenarioID: {query.lastError().text()}")

    query.exec("DROP TRIGGER IF EXISTS Update_HazardName")
    if not query.exec("""
        CREATE TRIGGER Update_HazardName
        AFTER UPDATE OF HazardName ON HazardSetup
        FOR EACH ROW
        BEGIN
            UPDATE HazardAnswers
            SET HazardName = NEW.HazardName
            WHERE HazardName = OLD.HazardName;
        END
    """):
        print(f"Error Update_ScenarioID: {query.lastError().text()}")

    query.exec("DROP TRIGGER IF EXISTS Delete_Scenario")
    if not query.exec("""
        CREATE TRIGGER Delete_Scenario
        AFTER DELETE ON ScenarioSetup
        FOR EACH ROW
        BEGIN
            DELETE FROM PerformanceAnswers
            WHERE ScenarioID = OLD.ScenarioID;

            DELETE FROM HazardAnswers
            WHERE ScenarioID = OLD.ScenarioID;
        END
    """):
        print(f"Error Delete_Scenario: {query.lastError().text()}")

    query.exec("DROP TRIGGER IF EXISTS Delete_Hazard")
    if not query.exec("""
        CREATE TRIGGER IF NOT EXISTS Delete_Hazard
        AFTER DELETE ON HazardSetup
        BEGIN
            DELETE FROM HazardAnswers
            WHERE HazardName = OLD.HazardName;
        END;
    """):
        print(f"Error Delete_Hazard: {query.lastError().text()}")


    ######### QUERIES FOR HAZARD ANSWERS TABLE UPDATE ##################

    query.exec("DROP TRIGGER IF EXISTS Insert_HazardAnswers_from_HazardSetup")
    if not query.exec("""
        CREATE TRIGGER IF NOT EXISTS Insert_HazardAnswers_from_HazardSetup
        AFTER INSERT ON HazardSetup
        BEGIN
            INSERT INTO HazardAnswers (HazardName, ScenarioID)
                SELECT NEW.HazardName, ScenarioID
                FROM ScenarioSetup;
        END;
    """):
        print(f"Error Insert_HazardAnswers_from_HazardSetup: {query.lastError().text()}")

    query.exec("DROP TRIGGER IF EXISTS Insert_HazardAnswers_from_ScenarioSetup")
    if not query.exec("""
        CREATE TRIGGER IF NOT EXISTS Insert_HazardAnswers_from_ScenarioSetup
        AFTER INSERT ON ScenarioSetup
        BEGIN
            INSERT INTO HazardAnswers (HazardName, ScenarioID)
                SELECT HazardName, NEW.ScenarioID
                FROM HazardSetup;
        END;
    """):
        print(f"Error Insert_HazardAnswers_from_ScenarioSetup: {query.lastError().text()}")

    Answers_Database.commit()

def setConsequencesTables(REFUSS_Database: QSqlDatabase, Answers_Database: QSqlDatabase):
    
    ConsequencesLibrary = fetch_table_from_database(REFUSS_Database, "IndicatorsLibrary")
    ConsequencesLibrary.set_index("IndicatorID", inplace = True)
        
    query = QSqlQuery(Answers_Database)

    for indicatorID, properties in ConsequencesLibrary.iterrows():
        ClassesLabels = properties["ClassesLabel"].split("; ")
        
        # Generate the SQL query to create the table with dynamic column names
        columns = []
        for label in ClassesLabels:
            columns.append(f"{label.replace(' ','')} REAL")
        
        columns_str = ", ".join(columns)
        
        if not query.exec(f"CREATE TABLE IF NOT EXISTS {indicatorID} ("
                f"ScenarioID INTEGER PRIMARY KEY, "
                f"{columns_str})"
                ):
            print(f"Error creating {indicatorID} table: {query.lastError().text()} in setConsequencesTables")

    for table_name, _ in ConsequencesLibrary.iterrows():
        # Drop the trigger if it exists
        query.exec(f"DROP TRIGGER IF EXISTS Upload_ScenarioID_at_{table_name}")

        # Create a trigger for the current table
        trigger_sql = f"""
            CREATE TRIGGER Upload_ScenarioID_at_{table_name}
            AFTER INSERT ON ScenarioSetup
            FOR EACH ROW
            BEGIN
                INSERT INTO {table_name} (ScenarioID) VALUES (NEW.ScenarioID);
            END
        """
        
        # Execute the trigger creation SQL
        if not query.exec(trigger_sql):
            print(f"Error creating trigger Upload_ScenarioID_at_{table_name}: {query.lastError().text()}")


    # Drop the trigger if it exists
    query.exec("DROP TRIGGER IF EXISTS Delete_Scenario_at_Consequences")

    # Construct the SQL statements for DELETE actions
    delete_statements = [
        f"DELETE FROM {table_name} WHERE ScenarioID = OLD.ScenarioID"
        for table_name, _ in ConsequencesLibrary.iterrows()
    ]

    # Join the DELETE statements with semicolons and line breaks
    delete_sql = ";\n".join(delete_statements)

    # Create a single trigger for ScenarioSetup
    trigger_sql = f"""
        CREATE TRIGGER Delete_Scenario_at_Consequences
        AFTER DELETE ON ScenarioSetup
        FOR EACH ROW
        BEGIN
            {delete_sql};
        END
    """

    # Execute the trigger creation SQL
    if not query.exec(trigger_sql):
        print(f"Error creating trigger Delete_Scenario_at_Consequences: {query.lastError().text()}")


    
    
    


   
def getREFUSSDatabase(REFUSS_Database: QSqlDatabase):

    query = QSqlQuery(REFUSS_Database)

    dimension_query = ("SELECT * FROM Dimensions", "Dimensions")
    objectives_query = ("SELECT * FROM Objectives", "Objectives")
    criteria_query = ("SELECT * FROM Criteria", "Criteria")
    metrics_query = ("SELECT * FROM Metrics", "Metrics")
    metrics_options_query = ("SELECT * FROM MetricsOptions", "MetricsOptions")

    all_queries = [dimension_query,
                    objectives_query,
                    criteria_query,
                    metrics_query,
                    metrics_options_query]

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

    return Results[0], Results[1], Results[2], Results[3], Results[4]

def ObjectivesFromDimension(REFUSS_Database: QSqlDatabase, dimension_id: int):
    
    query = QSqlQuery(REFUSS_Database)
    query.prepare("SELECT ObjectiveID, ObjectiveSubID, ObjectiveName FROM Objectives WHERE DimensionID = ?")
    query.addBindValue(dimension_id)
    query.exec()

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

def FillNewAnswersDatabase(AnswersDatabase: QSqlDatabase, metrics: pd.DataFrame):

    # Clean existing contents of the answers table
    tables = AnswersDatabase.tables()
    query = QSqlQuery(AnswersDatabase)
    for table in tables:
        query.exec(f"DELETE FROM {table}")

    query.clear()

    query = QSqlQuery(AnswersDatabase)
    query.prepare("INSERT INTO MetricAnswers (criteriaID, metricID) VALUES (:value1, :value2)")

    MetricsID = metrics["MetricID"]
    CriteriaID = metrics["CriteriaID"]

    for metric, criteria in zip(MetricsID, CriteriaID):
        query.bindValue(":value1", criteria)
        query.bindValue(":value2", metric)
        query.exec()

def save_answer_to_AnswersDatabase(AnswersDatabase: QSqlDatabase, metricID: str, new_answer: str, newcomment: str):
    query = QSqlQuery(AnswersDatabase)
    query.prepare("UPDATE MetricAnswers SET answer = :answer, comment = :comment WHERE metricID = :metricID")
    query.bindValue(":metricID", metricID)
    query.bindValue(":answer", new_answer)
    query.bindValue(":comment", newcomment)
    query.exec()
    
def fetch_table_from_database(Database, TableName):
    if not Database.isOpen():
        print("Failed to connect to the database.")
        sys.exit(1)

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