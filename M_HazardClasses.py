from PySide6.QtWidgets import (QComboBox, QHBoxLayout, QVBoxLayout,  QWidget,  QSpacerItem, QSizePolicy,  QLabel, 
                               QFrame, QLabel, QTableView)

from PySide6.QtSql import QSqlDatabase, QSqlTableModel

from M_OperateDatabases import fetch_table_from_database
from M_IndicatorsSelection import flatten_dict
from M_Fonts import MyFont

from typing import Optional
import pandas as pd
import re

"""
This module defines diferent types of Hazards, as classes, and its associated operations.
One class corresponds to one methodology.

"""

def setHazardType(Methodology: str):

    if Methodology in ["P1", "V1"]:
        return ClassHazard(Methodology)
    elif Methodology == "B1":
        return BuildingHazard(Methodology)

class ClassHazard:
    def __init__(self,
                 Methodology: str,
                 ClassesValues: Optional[list] = None,
                 UnitType: Optional[int] = None,
                 ):
        """_summary_

        Args:
            ClassesValues (list): Provide the hazard values for each class, from the lower to the higer class, i.e, lower hazard to higher hazard.
            ValuesType (int): 1 for percentage, 2 for value
            Methodology (int): Choose methodology to calculate the hazard
                P1: Pedestrian hazard by DEFRA (2005)
                V1: Vehicles hazard by Martinez et al (2017)
        """       
        self.MethodologyNrClasses = {"P1": 4,
                                     "P2": 3,
                                     "V1": 3}
         
        if ClassesValues is None or ClassesValues == []:
            #raise TypeError("ClassHazards: ClassesValues is None, must be a list with values")
            pass
        
        if UnitType != 1 and UnitType != 2:
            raise TypeError("ClassHazards: ValuesType must be 1 (for %) or 2 (for real)")
        
        if Methodology not in self.MethodologyNrClasses.keys():
            raise TypeError("ClassHazards: Methodology not available...")
        
        if len(ClassesValues) != self.MethodologyNrClasses[Methodology] :
            raise TypeError("ClassHazards: Number of class values does not match the number of classes of the methodlogy")
       
        self.values = ClassesValues
        self.methodology = Methodology
        self.unittype = UnitType
       
        self.ClassesWeights = self.getClassesWeights()
    
    def getNumberOfClasses(self):
        return self.MethodologyNrClasses[self.methodology]
    
    def getClassesWeights(self):
        if self.methodology == 'P1':                #Pedestrian hazard by DEFRA (2005)
            ClassesWeights = [("Low",       1.0),
                              ("Moderate",    0.4),
                              ("High",        0.1),
                              ("Very High",   0.0)]
        
        elif self.methodology in ['V1', 'P2']:              #Vehicles hazard by Martinez et al (2017)
            ClassesWeights = [("Low",       1.0),
                              ("Moderate",    0.4),
                              ("High",        0.0)]
        
        else:
            #Space for new methodologies
            pass

        return ClassesWeights
        
    def calculateHazard(self):
        Hazard = 0
        
        if self.unittype == 1:      #percentage
            denominator = 100
        elif self.unittype == 2:    #real
            denominator = sum(self.values)
        
        for index, value in enumerate(self.values):
            ##############
            ### VERIFICAR QUE A SOMA DOS VALORES DEVERA SER IGUAL AO DENOMINADOR, cc devolve erro ####
            ##############
            classvalue = self.values[index] * self.ClassesWeights[index][1] / denominator   
            Hazard += classvalue
        return round(Hazard, 2)

class BuildingHazard:
    def __init__(self,
                 Methodology: str,
                 UserCustomUses: pd.DataFrame = None,
                 BuildingAnswers: pd.DataFrame = None,
                 ):
        
        """_summary_

        Args:
            Methodology (str): Choose methodology to calculate the hazard
                B1: Huizinga, J., De Moel, H., Szewczyk, W. (2017) https://publications.jrc.ec.europa.eu/repository/bitstream/JRC105688/global_flood_depth-damage_functions__10042017.pdf
            UserBuildingUsesOnMethodology (pd.DataFrame): Dataframe from the B1UsesSetup table containing the custom building uses and its associated methodology class.
            To be converted to a dictionary as follows:
                e.g. {"COMMERCIAL": ["TERCIARY", "EQUIPMENT"]}
            UserBuilingsSize (dict): Dictionay containing as keys the user building classes and as element its quantitiave value (for example, total area or number of buildings with that class)
                e.g. {"TERCIARY": 100, "EQUIPMENT": 20}           
        """
        
        MethodologyNrClasses = {"B1": 3}
        
        MethodologyUses = {"B1": ["RESIDENTIAL", "COMMERCIAL", "INDUSTRIAL"]}
        
        self.Methodology = Methodology
        
        self.CustomUses = UserCustomUses.copy(deep=True)
        self.CustomUses["MethodologyClass"] = self.CustomUses["MethodologyClass"].str.upper()

        self.CustomUses_convert = dict(zip(self.CustomUses["CustomUse"].str.upper(), self.CustomUses["MethodologyClass"]))
        
        self.Values = BuildingAnswers.copy(deep=True)
        self.Values["BuildingUse"] = self.Values["BuildingUse"].str.upper()
        self.Values.set_index("BuildingUse", inplace = True)
        
        if self.Methodology not in MethodologyNrClasses.keys():
            raise TypeError("BuildingHazard: Methodology not available...")
        
        self.methodology_uses_list = UserCustomUses["MethodologyClass"].unique().tolist()
        self.custom_uses_list = self.CustomUses["CustomUse"].str.upper().unique().tolist()
        
        for use in self.CustomUses_convert.values():
            if use not in MethodologyUses[self.Methodology]:
                raise TypeError("BuildingHazard: Building uses don't match the methodology")

        self.MethodologyCurves, self.MethodologyDepths = self.getMethodologyCurves()
        
        self.MethodologyNormalizedSetps = self.getMethodologySteps()
        
        # Invert and normalize the curves between 0 and 1
        self.NormalizedCurves = {}
        for class_name, values in self.MethodologyCurves.items():
            inverted_values = [1 - value for value in values]
            max_value = max(inverted_values)
            normalized_values = [value / max_value for value in inverted_values]
            self.NormalizedCurves[class_name] = normalized_values       
        
        """"   
            Plot MethodologyCurves
            for class_name, values in self.NormalizedCurves.items():
                plt.plot(self.MethodologyDepths, values, label=class_name)
                
            for class_name, values in self.MethodologyCurves.items():
                plt.plot(self.MethodologyDepths, values, '--', label=class_name)

            Add labels and title
            plt.xlabel('Methodology Depths')
            plt.ylabel('Curve Values')
            plt.title('Methodology Curves')

            Add legend
            plt.legend()

            Show the plot
            plt.show()
        """
    
    def calculateHazard(self):
        
        CustomUseAffectedFraction = pd.DataFrame(index = self.custom_uses_list, columns = self.Values.columns)
        CustomUseAffectedRating = pd.DataFrame(index = self.custom_uses_list, columns = self.Values.columns)
        
        TotalBuildingSize = self.Values.values.sum()
                
        for CustomUse, Values in self.Values.iterrows():
            self.Values.at[CustomUse, "TotalCustomUseSize"] = sum(Values)
            self.Values.at[CustomUse, "FractionCustomUseSize"] = sum(Values) / TotalBuildingSize
            for column, value in Values.items():
                CustomUseAffectedFraction.at[CustomUse, column] = value / sum(Values)
        
        #print(f"CustomUseAffectedFraction: \n{CustomUseAffectedFraction}")
        
        for CustomUse, Values in CustomUseAffectedFraction.iterrows():
            for column, value in Values.items():
                CustomUseAffectedRating.at[CustomUse, column] = value * self.MethodologyNormalizedSetps.at[self.CustomUses_convert[CustomUse], column]
          
        # CustomUseAffectedRating = CustomUseAffectedFraction * self.MethodologyNormalizedSetps
        
        for CustomUse, Values in CustomUseAffectedRating.iterrows():
            CustomUseAffectedRating.at[CustomUse, "TotalCustomUseRating"] = sum(Values) * self.Values.at[CustomUse, "FractionCustomUseSize"]

        #print(f"CustomUseAffectedRating: {CustomUseAffectedRating}")       
        
        TotalRating = CustomUseAffectedRating["TotalCustomUseRating"].values.sum()
        
        return round(TotalRating, 3)

    def getMethodologyCurves(self):
        
        if self.Methodology == 'B1':        #Huizinga, J., De Moel, H., Szewczyk, W. (2017)
            curves = {
                    "RESIDENTIAL": [0.00, 0.25, 0.40, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00],
                    "COMMERCIAL": [0.00, 0.15, 0.30, 0.45, 0.55, 0.75, 0.90, 1.00, 1.00],
                    "INDUSTRIAL": [0.00, 0.15, 0.27, 0.40, 0.52, 0.70, 0.85, 1.00, 1.00]
                    }
            depths = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0]
            
        return curves, depths

    def getMethodologySteps(self):
        
        if self.Methodology == 'B1':        #Huizinga, J., De Moel, H., Szewczyk, W. (2017)
            
            WaterClasses = ("Very Low", "Low", "Moderate", "High", "Very High")
            WaterDepths = ([0.0, 0.2], [0.2, 0.5], [0.5, 1.0], [1.0, 1.5], [1.5, 2.0])
            NormalizedDamage = {
                "RESIDENTIAL": (1, 0.75, 0.60, 0.50, 0.40),
                "COMMERCIAL": (1, 0.85, 0.70, 0.55, 0.45),
                "INDUSTRIAL": (1, 0.85, 0.73, 0.60, 0.48)
                }

            return pd.DataFrame.from_dict(NormalizedDamage, orient='index', columns=WaterClasses)
       
    def getMethodologyUse(self, value):
        for key, values in self.BuildingsRelationMethodology.items():
            if value in values:
                return key

class Indicator:
        
    def __init__(self, indicator_id: str, indicators: pd.DataFrame, answers_db: QSqlDatabase):
        self.indicator_id = indicator_id
        
        indicators_classes = indicators['indicators_classes']
        self.indicator_library = indicators['indicators_library'].loc[self.indicator_id]
        
        self.class_id = class_id = re.sub(r'\d', '', self.indicator_id)
        self.class_name = self.indicator_library['IndicatorClass']
        
        self.classes_nr = self.indicator_library['ClassesNr']
        self.classes_labels = self.indicator_library['ClassesLabel'].split("; ")
        self.show_name = self.indicator_library['ShowName']
        self.reference = self.indicator_library['Reference']
        self.possible_units = self.indicator_library['PossibleUnits'].split(";")
        
        self.unit = self.possible_units[0]
        
        self._selected = False
        
        self.answers_db = answers_db
    
        
        self.setup_layout = self.create_indicators_setup_widgets()
        self.scenarios_tableview = {}
        
        self.setup_model = QSqlTableModel(db = self.answers_db)
        self.answers_model = QSqlTableModel(db = self.answers_db)
 
    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if self._selected != value:
            self._selected = value
        
            if value == True:
                #print(f"{self.indicator_id} selected!")       
                pass      
            else:
                #print(f"{self.indicator_id} deselected!")
                pass 
        
    def create_indicators_setup_widgets(self):
        indicator_widget = QWidget()
        indicator_widget.setObjectName(self.indicator_id)
        indicator_layout = QVBoxLayout(indicator_widget)
        indicator_layout.setContentsMargins(0, 0, 0, 0)
        
        indicator_text = f'Methodology: {self.reference}'
        indicator_label = QLabel(indicator_text)
        indicator_label.setFont(MyFont(10, True))
        indicator_layout.addWidget(indicator_label)
        
        unit_layout = QHBoxLayout()
        indicator_layout.addLayout(unit_layout)
        
        if len(self.possible_units) > 1:
            unit_text = 'Select the data unit:'
            unit_label = QLabel(unit_text)
            unit_layout.addWidget(unit_label)
            
            model = QSqlTableModel(db = self.answers_db)
            model.setTable("IndicatorsSetup")
            model.select()
            
            unit_combo_box = QComboBox()
            unit_combo_box.addItems(self.possible_units)
            # Find the corresponding unit in the model
            model_column_name = "IndicatorUnit"
            model_row = find_model_row(model, 'IndicatorID', self.indicator_id)
            
            if model_row >= 0:
                # Get the unit value from the model
                initial_unit_value = model.data(model.index(model_row, model.fieldIndex(model_column_name)))
                if initial_unit_value in self.possible_units:
                    initial_index = self.possible_units.index(initial_unit_value)
                    unit_combo_box.setCurrentIndex(initial_index)
                else:
                    update_model(0, self.indicator_id, unit_combo_box, model)

            unit_combo_box.currentIndexChanged.connect(lambda index: update_model(index, self.indicator_id, unit_combo_box, model))
            unit_layout.addWidget(unit_combo_box)
            
        else:
            unit_text = f'Data unit: {self.possible_units[0]}'
            unit_label = QLabel(unit_text)
            unit_layout.addWidget(unit_label)   
                
        if self.indicator_id in ["P1", "P2", "V1"]:
            pass
        elif self.indicator_id in ["B1"]:
            pass
        elif self.indicator_id in ["SRP1", "SRP2", "SRP3"]:
            pass
            
        return indicator_widget

    def set_scenario_widget(self, scenario_id):
        
        scenario_layout = QVBoxLayout()
        scenario_layout.setContentsMargins(0, 0, 0, 0)
        
        reference_label = QLabel(f'Methodology: {self.reference}')
        unit_label = QLabel(f'Data unit: {self.unit}')
        h_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        v_line = QFrame()
        v_line.setFrameShadow(QFrame.Plain)
        v_line.setLineWidth(1)
        v_line.setMidLineWidth(0)
        v_line.setFrameShape(QFrame.VLine)
        header_layout = QHBoxLayout()
        header_layout.addWidget(reference_label)
        header_layout.addChildWidget(v_line)
        header_layout.addWidget(unit_label)
        header_layout.addItem(h_spacer)
        
        scenario_model = QSqlTableModel(db = self.answers_db)
        scenario_model.setTable(self.indicator_id)
        scenario_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        scenario_model.setFilter(f"ScenarioID = '{scenario_id}'")
        scenario_model.select()
        
        scenarios_view = QTableView()
        scenarios_view.setModel(scenario_model)
        scenarios_view.setObjectName(f"{self.indicator_id}")
        # Hide first column (ScenarioID)
        scenarios_view.setColumnHidden(0, True)
        scenarios_view.setStyleSheet(
            "QTableView { background-color: white; border: none; }"
            "QHeaderView::section { background-color: #EDEDED; border: 1 px solid black; }"
            "QTableView::item { background-color: white; }"
            "QTableView::item:selected { background-color: #D3D3D3; color: black }"
            )
        # Hide the vertical header (row indexes)
        scenarios_view.verticalHeader().setVisible(False)        
        
        scenario_layout.addLayout(header_layout)
        scenario_layout.addWidget(scenarios_view)
        
        if self.indicator_id in ["B1"]:
            pass
        
        self.scenarios_tableview[scenario_id] = scenarios_view
        
        return self.scenarios_tableview[scenario_id]
         
    def set_selected_state(self, selected_indicators):
        if self.indicator_id in flatten_dict(selected_indicators):
            self._selected = True
        else:
            self._selected = False           
            
class All_Indicators(dict):
    
    def __init__(self):
        super().__init__()
        
        self.selected_indicators = self.get_selected_indicators()
        
    def update_selected_status(self, selected_indicators: list):
        for indicator_id, indicator in self.items():
            if indicator_id in flatten_dict(selected_indicators):
                indicator._selected = True
            else:
                indicator._selected = False
    
    def get_selected_indicators(self):
        selected_indicators = {}
        for indicator_id, indicator in self.items():
            if indicator._selected:
                if indicator.class_id not in selected_indicators.keys():
                    selected_indicators[indicator.class_id] = []
                selected_indicators[indicator.class_id].append(indicator_id)
            
        return selected_indicators
    
    def update_selected_units(self, answers_db):
        indicator_settings = fetch_table_from_database(answers_db, "IndicatorsSetup")
        indicator_settings.set_index('IndicatorID', inplace=True)
        
        for indicator_id, indicator in indicator_settings.iterrows():
            if indicator['IndicatorUnit']:
                self[indicator_id].indicator_unit = indicator['IndicatorUnit']    
           
def update_model(index, IndicatorID, combo_box, model):
    selected_value = combo_box.currentText()
    model_column = "IndicatorUnit"
    
    model_row = find_model_row(model, 'IndicatorID', IndicatorID)
    model.setData(model.index(model_row, model.fieldIndex(model_column)), selected_value)
    model.submitAll()

def find_model_row(model, model_column_name, search_name):
    # Find the row in the model where the model_column_name value is equal to search_name
    row = -1
    for i in range(model.rowCount()):
        if model.data(model.index(i, model.fieldIndex(model_column_name))) == search_name:
            row = i
            break
    return row          

if __name__ == '__main__':
    testPed = [732787.76, 57829.44, 115074.42, 1525.20]
    HazardPedestrian = ClassHazard(testPed, 2, 'P1').calculateHazard()
    print(HazardPedestrian)
    testVehic = [80.34, 4.39, 15.26]
    HazardVehicles = ClassHazard(testVehic, 1, 'V1').calculateHazard()
    print(HazardVehicles)
    
    ["RESIDENTIAL", "COMMERCIAL", "INDUSTRIAL"]
    
    "test buildings"
    MatchBuilingsUse = {"RESIDENTIAL": ["HABITACAO"],
                        "COMMERCIAL": ["TERCIARIO", "EQUIPAMENTO"],
                        "INDUSTRIAL": ["INDUSTRIAL", "LOGISTICO"]}
    
    BuildingsSize = {"HABITACAO": 84102,
                     "TERCIARIO": 111651,
                     "EQUIPAMENTO": 70687,
                     "INDUSTRIAL": 4919,
                     "LOGISTICO": 27307}        #IN AREA (m2)
    
    data = {
    'h': [0.2, 0.5, 1.0, 1.5, 2.0],
    'HABITACAO': [78321, 2866, 2618, 297, 0],
    'TERCIARIO': [47887, 20220, 32380, 10856, 309],
    'EQUIPAMENTO': [50155, 3134, 5081, 12316, 0],
    'INDUSTRIAL': [0, 0, 4919, 0, 0],
    'LOGISTICO': [5592, 17189, 2819, 1707, 0]
    }

    WaterDepth = pd.DataFrame(data)   
    
    BuildingHazardA = BuildingHazard("B1", MatchBuilingsUse, BuildingsSize, WaterDepth).calculateHazard()
    
    print(BuildingHazardA)
    