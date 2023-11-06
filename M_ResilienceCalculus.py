import pandas as pd

from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

from M_HazardClasses import ClassHazard
from M_OperateDatabases import fetch_table_from_database

def Caculate_ConsequencesRating(AnswersDatabase: QSqlDatabase,
                               IndicatorsLibrary: pd.DataFrame,
                               ScenarioSetup: pd.DataFrame,
                               IndicatorsSetup: pd.DataFrame):
       
    SelectedIndicators = IndicatorsSetup[IndicatorsSetup['SelectedState'] == 1]
            
    PerformanceConsequenceRating = pd.DataFrame(columns = ScenarioSetup.index, index = IndicatorsSetup.index)
            
    for ind_id, ind_prop in SelectedIndicators.iterrows():
        
        IndAns = fetch_table_from_database(AnswersDatabase, f"{ind_id}")
        IndAns.set_index("ScenarioID", inplace=True)        
        
        if not ind_id.startswith("SRP"):           
            ind_unit = ind_prop["SelectedUnit"]
        if "[%]" in ind_unit:
            unit_type = 1
        else:
            unit_type = 2
        
        if not ind_id.startswith(("SRP", "B1")):
            for scn_id, values in IndAns.iterrows():
                IndResilience = 0
                if any(value == '' for value in values):
                    IndResilience = None
                else:
                    values = values.astype(float).tolist()
                    IndResilience = ClassHazard(
                        Methodology = ind_id,
                        ClassesValues = values,
                        UnitType = unit_type).calculateHazard()
             
                PerformanceConsequenceRating.loc[ind_id, scn_id] = IndResilience
                
    return PerformanceConsequenceRating.T

def Calculate_FunctionalRating(Weights: pd.DataFrame, Metrics: pd.DataFrame, MetricsOptions: pd.DataFrame, MetricsAnswers:pd.DataFrame):

    def singlechoicescore(AnswerIndex = int, OptionsNumber = int):

        score = min(1, AnswerIndex/(OptionsNumber - 1))

        return round(score, 2)

    def multiplechoisescore(AnswersIndexes = list, OptionsNumber = int):

        if 0 in AnswersIndexes:
            score = 0
        else:
            score = len(AnswersIndexes)/(OptionsNumber - 1)   # -1 to not count the option index 0 (No, None, etc.)
        return round(score, 2)

    MetricsOptionsNumber = pd.DataFrame(index = Metrics.index, columns=['OptionsNumber'])

    for metricID, row in MetricsOptions.iterrows():
        OptionsNr = 0
        for column_name, value in row.items():
            if value:
                OptionsNr += 1
        MetricsOptionsNumber.loc[metricID, "OptionsNumber"] = OptionsNr

    MetricScore = pd.DataFrame(index = Metrics.index, columns=['Score', 'DimensionID', 'ObjectiveID', 'CriteriaID'])

    for metricID, row in MetricsAnswers.iterrows():
        answer_nr_options = MetricsOptionsNumber.loc[metricID, "OptionsNumber"]
        dimension_int = metricID.split('.')[0]
        objective_int = metricID.split('.')[1]
        criteria_int = metricID.split('.')[2]
        dimension_id = f"{dimension_int}"
        objective_id = f"{dimension_int}.{objective_int}"
        criteria_id = f"{dimension_int}.{objective_int}.{criteria_int}"
                
        if not row["answer"]:       # If no answer -> the answer does not count for the score -> the criteria cant reach rating 1
            score = 'NA'
        else:
            if Metrics.loc[metricID, "Answer_Type"] == "Single choice":
                    answer_index = int(row["answer"].split("_")[0])
                    score = singlechoicescore(answer_index, answer_nr_options)

            elif Metrics.loc[metricID, "Answer_Type"] == "Multiple choice":
                answer_indexes = []
                for answer in row["answer"].split(";"):
                    answer_indexes.append(int(answer.split("_")[0]))
                score = multiplechoisescore(answer_indexes, answer_nr_options)

        MetricScore.loc[metricID, "Score"] = score
        MetricScore.loc[metricID, "DimensionID"] = dimension_id
        MetricScore.loc[metricID, "ObjectiveID"] = objective_id
        MetricScore.loc[metricID, "CriteriaID"] = criteria_id
   
    CriteriaRating = MetricScore.drop_duplicates(subset = "CriteriaID").set_index("CriteriaID", drop=True).copy()
    CriteriaRating.drop("Score", axis = 1, inplace = True)
    CriteriaRating = CriteriaRating.join(Weights["Criteria"]["Weight"], how = "right")
    CriteriaRating["Rating"] = 0
    CriteriaRating["AnsweredMetrics"] = 0
    CriteriaRating["TotalMetrics"] = 0
    CriteriaRating["Space"] = 0
   
    for metricID, prop in MetricScore.iterrows():
        CriteriaRating.at[prop["CriteriaID"], "TotalMetrics"] += 1
        if prop["Score"] != 'NA':
            CriteriaRating.at[prop["CriteriaID"], "AnsweredMetrics"] += 1
            CriteriaRating.at[prop["CriteriaID"], "Rating"] += prop["Score"]            
    
    CriteriaRating["Completness"] = CriteriaRating["AnsweredMetrics"] / CriteriaRating["TotalMetrics"]
    CriteriaRating["Missing"] = 1 - CriteriaRating["Completness"]
    CriteriaRating["Rating"] = CriteriaRating["Rating"] / CriteriaRating["TotalMetrics"]
    CriteriaRating["Space"] = CriteriaRating["Completness"] - CriteriaRating["Rating"]
    
    print(CriteriaRating)
    
    ObjectivesRating = MetricScore.drop_duplicates(subset = "ObjectiveID").set_index("ObjectiveID", drop=True).copy()
    ObjectivesRating.drop("Score", axis = 1, inplace = True)
    ObjectivesRating.drop("CriteriaID", axis = 1, inplace = True)
    ObjectivesRating = ObjectivesRating.join(Weights["Objectives"]["Weight"].loc[ObjectivesRating.index], how = "right")
    ObjectivesRating["Completness"] = 0
    ObjectivesRating["Missing"] = 0
    ObjectivesRating["Rating"] = 0
    ObjectivesRating["Space"] = 0
    
    for obj_id, obj_prop in ObjectivesRating.iterrows():
        completness = 0
        missing = 0
        rating = 0
        space = 0
        w_sum = 0
        for crit_id, crit_prop in CriteriaRating[CriteriaRating["ObjectiveID"] == obj_id].iterrows():
            completness += crit_prop["Completness"] * crit_prop["Weight"]
            missing += crit_prop["Missing"] * crit_prop["Weight"]
            rating += crit_prop["Rating"] * crit_prop["Weight"]
            space += crit_prop["Space"] * crit_prop["Weight"]
            w_sum += crit_prop["Weight"]
        ObjectivesRating.at[obj_id, "Completness"] = completness / w_sum  
        ObjectivesRating.at[obj_id, "Missing"] = missing / w_sum
        ObjectivesRating.at[obj_id, "Rating"] = rating / w_sum
        ObjectivesRating.at[obj_id, "Space"] = space / w_sum           
    
    print(ObjectivesRating)        
  
    DimensionRating = MetricScore.drop_duplicates(subset = "DimensionID").set_index("DimensionID", drop=True).copy()
    DimensionRating.drop("Score", axis = 1, inplace = True)
    DimensionRating.drop("ObjectiveID", axis = 1, inplace = True)
    DimensionRating.drop("CriteriaID", axis = 1, inplace = True)
    DimensionRating = DimensionRating.join(Weights["Dimensions"]["Weight"].loc[DimensionRating.index], how = "right")
    DimensionRating["Completness"] = 0
    DimensionRating["Missing"] = 0
    DimensionRating["Rating"] = 0
    DimensionRating["Space"] = 0
    
    for dim_id, dim_prop in DimensionRating.iterrows():
        completness = 0
        missing = 0
        rating = 0
        space = 0
        w_sum = 0
        for obj_id, obj_prop in ObjectivesRating[ObjectivesRating["DimensionID"] == dim_id].iterrows():
            completness += obj_prop["Completness"] * obj_prop["Weight"]
            missing += obj_prop["Missing"] * obj_prop["Weight"]
            rating += obj_prop["Rating"] * obj_prop["Weight"]
            space += obj_prop["Space"] * obj_prop["Weight"]
            w_sum += obj_prop["Weight"]
        DimensionRating.at[dim_id, "Completness"] = completness / w_sum
        DimensionRating.at[dim_id, "Missing"] = missing / w_sum
        DimensionRating.at[dim_id, "Rating"] = rating / w_sum
        DimensionRating.at[dim_id, "Space"] = space / w_sum  

    print(DimensionRating) 

    return DimensionRating, ObjectivesRating, CriteriaRating

def Calculate_Completness(Functional_Answers):

    MetricAnswerStatus = pd.DataFrame(index = Functional_Answers.index, columns=['AnswerStatus', 'Dimension', 'Objective', 'ObjectiveID'])

    for metricID, metric in Functional_Answers.iterrows():
        dimension = metricID.split('.')[0]
        objective = metricID.split('.')[1]
        if metric["answer"]:
            MetricAnswerStatus.at[metricID, "AnswerStatus"] = 1
        else:
            MetricAnswerStatus.at[metricID, "AnswerStatus"] = 0
        MetricAnswerStatus.at[metricID, "Dimension"] = dimension
        MetricAnswerStatus.at[metricID, "Objective"] = objective
        MetricAnswerStatus.at[metricID, "ObjectiveID"] = f'{dimension}.{objective}'

    MetricAnswerStatus.set_index("ObjectiveID", inplace = True)
    
    # Group by Objective and calculate the summary statistics
    summary_df = MetricAnswerStatus.groupby('ObjectiveID').agg({'AnswerStatus': ['count', 'sum', 'mean']})

    # Rename the columns
    summary_df.columns = ['CountOptions', 'CountAnswers', 'Completness']
    summary_df["Completness"] = summary_df["Completness"] * 100
    summary_df["Missing"] = 100 - summary_df["Completness"]

    return summary_df