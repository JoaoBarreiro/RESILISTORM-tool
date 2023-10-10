import pandas as pd

from M_HazardClasses import ClassHazard

def Caculate_PerformanceConsequencesRating(HazardLibrary: pd.DataFrame, HazardSetup: pd.DataFrame, HazardAnswers: pd.DataFrame):
    
    HazardAnswers.set_index("HazardName", inplace = True)
    HazardLibrary.set_index("ShowName", inplace = True)
    HazardSetup.set_index("HazardName", inplace = True)
    
    AvailableHazards = HazardAnswers.index.unique().tolist()
    AvailableScenarios = HazardAnswers["ScenarioName"].unique().tolist()
    
    AvailabeHazardsID = HazardLibrary.loc[HazardLibrary.index.isin(AvailableHazards), "ID"].tolist()
    
    PerformanceConsequenceRating = pd.DataFrame(columns = AvailableHazards, index = AvailableScenarios)
    
    for Hazard, row in HazardAnswers.iterrows():
        HazardID = HazardLibrary.loc[Hazard, "ID"]
        HazardUnit = HazardSetup.loc[Hazard, "HazardUnit"]
        NrClasses = int(HazardLibrary.loc[Hazard, "NrClasses"])
        
        row_Scenario = row[0]
        if HazardUnit == "%":
            AnswerType = 1
        elif HazardUnit == "Area":
            AnswerType = 2
        
        if HazardID in ["V1", "P1"]:
            HazardResilience = 0
            # Verifies that all the class values are answered
            for value in row[1:1+NrClasses]:
                if value == '':
                    HazardResilience = None
                    break
            if HazardResilience != None:    
                classValues = row[1:1+NrClasses].astype(float).tolist()
                HazardResilience = ClassHazard(classValues, AnswerType, HazardID).calculateHazard()
            
        PerformanceConsequenceRating.loc[row_Scenario, Hazard] = HazardResilience
    
    column_names = dict(zip(AvailableHazards,AvailabeHazardsID))
    
    PerformanceConsequenceRating = PerformanceConsequenceRating.rename(columns = column_names)
            
    return PerformanceConsequenceRating

def Calculate_FunctionalMetricsRating(Metrics: pd.DataFrame, MetricsOptions: pd.DataFrame, MetricsAnswers:pd.DataFrame):

    def singlechoicescore(AnswerIndex = int, OptionsNumber = int):

        score = min(1, AnswerIndex/(OptionsNumber - 1))

        return round(score, 2)

    def multiplechoisescore(AnswersIndexes = list, OptionsNumber = int):

        if 0 in AnswersIndexes:
            score = 0
        else:
            score = len(AnswersIndexes)/(OptionsNumber - 1)   # -1 to not count the option index 0 (No, None, etc.)
        return round(score, 2)

    Metrics.set_index("MetricID", inplace = True)
    MetricsAnswers.set_index("metricID", inplace = True)
    MetricsOptions.set_index("MetricID", inplace = True)

    MetricsOptionsNumber = pd.DataFrame(index = Metrics.index, columns=['OptionsNumber'])

    for MetricID, row in MetricsOptions.iterrows():
        OptionsNr = 0
        for column_name, value in row.items():
            if value:
                OptionsNr += 1
        MetricsOptionsNumber.loc[MetricID, "OptionsNumber"] = OptionsNr

    MetricScore_df = pd.DataFrame(index = Metrics.index, columns=['AnswerScore'])

    for MetricID, row in MetricsAnswers.iterrows():
        answer_nr_options = MetricsOptionsNumber.loc[MetricID, "OptionsNumber"]
        if not row["answer"]:
            score = 0
        else:
            if Metrics.loc[MetricID, "Answer_Type"] == "Single choice":
                    answer_index = int(row["answer"].split("_")[0])
                    score = singlechoicescore(answer_index, answer_nr_options)

            elif Metrics.loc[MetricID, "Answer_Type"] == "Multiple choice":
                answer_indexes = []
                for answer in row["answer"].split(";"):
                    answer_indexes.append(int(answer.split("_")[0]))
                score = multiplechoisescore(answer_indexes, answer_nr_options)

        MetricScore_df.loc[MetricID, "AnswerScore"] = score

    df = pd.DataFrame(MetricScore_df)

    # Extract the Dimension and Objective from the MetricID
    df['Dimension'] = df.index.str.split('.').str[0]
    df['Objective'] = df.index.str.split('.').str[1]
    df['Criteria'] = df.index.str.split('.').str[1] + '.' + df.index.str.split('.').str[2]

    # Filter the dataframe for Dimension 1
    Functional_df = df[df['Dimension'] == '1']

    DimensionResileinceSummary_df = Functional_df.groupby('Dimension').agg({
        'AnswerScore': ['count', 'sum', 'mean']
    })

    # Reset the index and rename the columns
    DimensionResileinceSummary_df.reset_index(inplace=True)
    DimensionResileinceSummary_df.columns = ['Dimension', 'Count', 'SumAnswerScores', 'MeanResilience']

    # Group by Objective and calculate the summary statistics
    ObjectivesSummary_df = Functional_df.groupby('Objective').agg({
        'AnswerScore': ['count', 'sum', 'mean']
    })

    # Reset the index and rename the columns
    ObjectivesSummary_df.reset_index(inplace=True)
    ObjectivesSummary_df.columns = ['Objective', 'Count', 'SumAnswerScores', 'MeanAnswerScores']

    # Group by Criteria and calculate the summary statistics
    CriteriaSummary_df = Functional_df.groupby('Criteria').agg({
        'AnswerScore': ['count', 'sum', 'mean']
    })

    # Reset the index and rename the columns
    CriteriaSummary_df.reset_index(inplace=True)
    CriteriaSummary_df.columns = ['Criteria', 'Count', 'SumAnswerScores', 'MeanAnswerScores']

    return DimensionResileinceSummary_df, ObjectivesSummary_df, CriteriaSummary_df


def Calculate_Completness(MetricsAnswersDataFrame):

    MetricAnswerStatus_df = pd.DataFrame(columns=['MetricID', 'AnswerStatus'])

    for index, row in MetricsAnswersDataFrame.iterrows():
        if row["answer"]:
            MetricAnswerStatus_df.loc[len(MetricAnswerStatus_df)] = [row["metricID"], 1]
        else:
            MetricAnswerStatus_df.loc[len(MetricAnswerStatus_df)] = [row["metricID"], 0]

    df = pd.DataFrame(MetricAnswerStatus_df)

    # Extract the Dimension and Objective from the MetricID
    df['Dimension'] = df['MetricID'].str.split('.').str[0]
    df['Objective'] = df['MetricID'].str.split('.').str[1]

    # Filter the dataframe for Dimension 1
    filtered_df = df[df['Dimension'] == '1']

    # Group by Objective and calculate the summary statistics
    summary_df = filtered_df.groupby('Objective').agg({
        'MetricID': 'count',
        'AnswerStatus': ['sum', 'mean']
    })

    # Reset the index and rename the columns
    summary_df.reset_index(inplace=True)
    summary_df.columns = ['Objective','Count', 'TotalAnswerStatus', 'MeanAnswerStatus']
    summary_df["MeanAnswerStatus"] = summary_df["MeanAnswerStatus"] * 100
    
    summary_df["Objective"] = summary_df["Objective"].astype(int)
    
    #print(summary_df)

    return summary_df