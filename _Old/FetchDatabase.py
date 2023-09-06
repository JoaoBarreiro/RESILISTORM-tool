import pandas as pd
from PySide6.QtSql import QSqlDatabase, QSqlQuery

def REFUSS_Database(REFUSS_Database: QSqlDatabase):

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