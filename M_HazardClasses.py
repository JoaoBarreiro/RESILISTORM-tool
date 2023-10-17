from PySide6.QtWidgets import (QComboBox, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QInputDialog, QSpacerItem, QSizePolicy, QDialog, QLabel, 
                               QScrollArea, QMessageBox, QFrame, QFormLayout, QLineEdit, QCheckBox, QRadioButton, QLabel, QButtonGroup,
                               QTableView)

from PySide6.QtCore import Qt, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

import M_OperateDatabases

from M_IndicatorsSelection import flatten_dict

from M_Fonts import MyFont

from matplotlib import pyplot as plt
from typing import Optional
import pandas as pd
import numpy as np
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
    def __init__(self, Methodology: str,
                 ClassesValues: Optional[list] = None,
                 ValuesType: Optional[int] = None,
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
                                     "V1": 3}
         
        if ClassesValues is None or ClassesValues == []:
            #raise TypeError("ClassHazards: ClassesValues is None, must be a list with values")
            pass
        
        if ValuesType != 1 and ValuesType != 2:
            raise TypeError("ClassHazards: ValuesType must be 1 (for %) or 2 (for real)")
        
        if Methodology not in self.MethodologyNrClasses.keys():
            raise TypeError("ClassHazards: Methodology not available...")
        
        if len(ClassesValues) != self.MethodologyNrClasses[Methodology] :
            raise TypeError("ClassHazards: Number of class values does not match the number of classes of the methodlogy")
       
        self.values = ClassesValues
        self.methodology = Methodology
        self.datatype = ValuesType
       
        self.ClassesWeights = self.getClassesWeights()
    
    def getNumberOfClasses(self):
        return self.MethodologyNrClasses[self.methodology]
    
    def getClassesWeights(self):
        if self.methodology == 'P1':                #Pedestrian hazard by DEFRA (2005)
            ClassesWeights = [("Low",       1.0),
                              ("Moderate",    0.4),
                              ("High",        0.1),
                              ("Very High",   0.0)]
            
        elif self.methodology == 'V1':              #Vehicles hazard by Martinez et al (2017)
            ClassesWeights = [("Low",       1.0),
                              ("Moderate",    0.4),
                              ("High",        0.0)]
        
        else:
            #Space for new methodologies
            pass

        return ClassesWeights
        
    def calculateHazard(self):
        Hazard = 0
        
        if self.datatype == 1:      #percentage
            denominator = 100
        elif self.datatype == 2:    #real
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
                 UserBuildingUsesOnMethodology: Optional[dict] = None,
                 UserBuilingsSize: Optional[dict] = None,
                 WaterHeightOnBuildings: Optional[dict] = None):
        
        """_summary_

        Args:
            Methodology (str): Choose methodology to calculate the hazard
                B1: Huizinga, J., De Moel, H., Szewczyk, W. (2017) https://publications.jrc.ec.europa.eu/repository/bitstream/JRC105688/global_flood_depth-damage_functions__10042017.pdf
            UserBuildingUsesOnMethodology (dict): Dictionay containing as keys the building uses form the selected metholodogy and as element a list of the user building uses that match the methodology uses. Use only CAPITAL LETTERS FOR STRNINGS
                e.g. {"COMMERCIAL": ["TERCIARY", "EQUIPMENT"]}
            UserBuilingsSize (dict): Dictionay containing as keys the user building classes and as element its quantitiave value (for example, total area or number of buildings with that class)
                e.g. {"TERCIARY": 100, "EQUIPMENT": 20}
            #WaterHeightOnBuildings (dict): Dictionary containg as keys the user building classes and as elements a dataframe where 1st column is maximum water height (in meters) and 2nd column is the number/area of buildings affected 
             #   e.g. {"TERCIARY": pd.DataFrame({'MaxWater': [0, 0.2, 0.5], 'Value': [90, 5, 5]}), ...}
            
        """
        
        MethodologyNrClasses = {"B1": 3}
        
        MethodologyUses = {"B1": ["RESIDENTIAL", "COMMERCIAL", "INDUSTRIAL"]}
        
        if Methodology not in MethodologyNrClasses.keys():
            raise TypeError("BuildingHazard: Methodology not available...")
        
        if not all(key in MethodologyUses.get(Methodology, []) for key in UserBuildingUsesOnMethodology.keys()):
            raise TypeError("BuildingHazard: Building uses don't match the methodology")          
        
        self.UserBuildingsUse = []
        for list in UserBuildingUsesOnMethodology.values():
            for UserBuildingType in list:
                self.UserBuildingsUse.append(UserBuildingType)

        # if UserBuilingsSize.keys() not in self.UserBuildingsUse:
        #     raise TypeError("BuildingHazard: UserBuildingSize dont match uses given in UserBuildingUsesOnMethodology")          
         
        # if WaterHeightOnBuildings.keys() not in self.UserBuildingsUse:
        #     raise TypeError("BuildingHazard: WaterHeightOnBuildings dont match uses given in UserBuildingUsesOnMethodology")          
            
        self.Methodology = Methodology
        self.BuildingsRelationMethodology = UserBuildingUsesOnMethodology
        self.UserBuildingsSize = UserBuilingsSize
        self.WaterLevels = WaterHeightOnBuildings.iloc[:, :1]
        self.BuildingsAffected = WaterHeightOnBuildings.iloc[:, 1:]
    
        self.MethodologyCurves, self.MethodologyDepths = self.getMethodologyCurves()

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

        WaterDepthLabel = next(iter(self.WaterLevels))
    
    def calculateHazard(self):
        
        # TotalBuildingSize is the sum of the buildings sizes (in area or number, depending on the user input)             
        TotalBuildingSize = sum(self.UserBuildingsSize.values())
        
        #BuildingsUseFraction is the ratio of buidling of each use over the total number of buildings
        BuildingsUseFraction = {}
        
        # BuildingsAffectedFraction is the fraction of buildings affected in each use clas
        BuildingsAffectedFraction = pd.DataFrame()
        for Use, Affected in self.BuildingsAffected.items():
            TotalByUse = sum(Affected)
            BuildingsUseFraction[Use] = TotalByUse / TotalBuildingSize
            BuildingsAffectedFraction[Use] = Affected/TotalByUse
            
        # NormalizedDamage is the BuildingsAffectedFraction multiplied by the damagefactor (interpolated from the methodlogy curves)
        NormalizedDamage = pd.DataFrame()
        for Use, FractionAffected in BuildingsAffectedFraction.items():
            if Use in self.UserBuildingsUse:
                MethodologyUse = self.getMethodologyUse(Use)                #Get the methodology use associated to the User given use
                damage_factor = (np.interp(self.WaterLevels, self.MethodologyDepths, self.NormalizedCurves[MethodologyUse])).flatten().tolist()  
                NormalizedDamage[Use] = FractionAffected * damage_factor
        
        # HazardByUse is the sum of the contributions of all fractions of each use
        HazardByUse = {}
        for key, values in NormalizedDamage.items():
            HazardByUse[key] = sum(values)
        
        #HazardContributionByUse is the product of each Hazard by Building Use with the Building Use Fraction 
        HazardContributionByUse = {}
        for Use in HazardByUse.keys():
            HazardContributionByUse[Use] = HazardByUse[Use] * BuildingsUseFraction[Use]
            
        TotalHazard = sum(HazardContributionByUse.values())
        
        return round(TotalHazard, 2)

    def getMethodologyCurves(self):
        
        if self.Methodology == 'B1':        #Huizinga, J., De Moel, H., Szewczyk, W. (2017)
            curves = {
                    "RESIDENTIAL": [0.00, 0.25, 0.40, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00],
                    "COMMERCIAL": [0.00, 0.15, 0.30, 0.45, 0.55, 0.75, 0.90, 1.00, 1.00],
                    "INDUSTRIAL": [0.00, 0.15, 0.27, 0.40, 0.52, 0.70, 0.85, 1.00, 1.00]
                    }
            depths = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0]
            
        return curves, depths

    def getMethodologyUse(self, value):
        for key, values in self.BuildingsRelationMethodology.items():
            if value in values:
                return key



class Indicator:
    
    selection_state_changed = Signal(bool)
    
    def __init__(self, indicator_id: str, indicators: pd.DataFrame, answers_db: QSqlDatabase):
        self.indicator_id = indicator_id
        
        indicators_classes = indicators['indicators_classes']
        self.indicator_library = indicators['indicators_library'].loc[self.indicator_id]
        
        self.indicator_class = class_id = re.sub(r'\d', '', self.indicator_id)
        
        self.classes_nr = self.indicator_library['ClassesNr']
        self.classes_labels = self.indicator_library['ClassesLabel'].split("; ")
        self.show_name = self.indicator_library['ShowName']
        self.reference = self.indicator_library['Reference']
        self.possible_units = self.indicator_library['PossibleUnits'].split(";")
        
        self.answers_db = answers_db
        
        self._selected = False
        
        self.setup_widget = self.create_indicators_setup_widgets()
        self.scenarios_view = {}
        
        self.setup_model = QSqlTableModel(db = self.answers_db)
        self.answers_model = QSqlTableModel(db = self.answers_db)
 
    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if self._selected != value:
            self._selected = value
            #self.selection_state_changed.emit(value)
            
            existing_scenarios = M_OperateDatabases.getUniqueColumnValues(self.answers_db, "ScenarioSetup", "ScenarioID")
            
            if value == True:
                print(f"{self.indicator_id} selected!")
                                
                self.setup_widget.show()
                for scenario in existing_scenarios:
                    self.scenarios_view[scenario].show()
                
            else:
                print(f"{self.indicator_id} deselected!")
                
                self.setup_widget.hide()
                for scenario in existing_scenarios:
                    self.scenarios_view[scenario].show()
        
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
        
        scenario_model = QSqlTableModel(db = self.answers_db)
        scenario_model.setTable(self.indicator_id)
        scenario_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        scenario_model.setFilter(f"ScenarioID = '{scenario_id}'")
        scenario_model.select()
        
        self.scenarios_view[scenario_id] = QTableView()
        self.scenarios_view[scenario_id].setModel(scenario_model)
        self.scenarios_view[scenario_id].setObjectName(f"{self.indicator_id}")
        self.scenarios_view[scenario_id].setColumnHidden(0, True)            
            
        return self.scenarios_view[scenario_id]

    def set_selected_state(self, selected_indicators):
        if self.indicator_id in flatten_dict(selected_indicators):
            self._selected = True
        else:
            self._selected = False
            
     
# def create_indicators_setup_widgets(IndicatorsLibrary: pd.DataFrame, IndicatorID: str, AnswersDatabase: QSqlDatabase):
    
#     indicator_widget = QWidget()
#     indicator_widget.setObjectName(IndicatorID)
#     indicator_layout = QVBoxLayout(indicator_widget)
#     indicator_layout.setContentsMargins(0, 0, 0, 0)
    
#     indicator_data = IndicatorsLibrary.loc[IndicatorID]
    
#     indicator_text = f'Methodology: {indicator_data["Reference"]}'
#     indicator_label = QLabel(indicator_text)
#     indicator_label.setFont(MyFont(10, True))
#     indicator_layout.addWidget(indicator_label)
    
#     unit_layout = QHBoxLayout()
#     indicator_layout.addLayout(unit_layout)
    
#     possible_units = indicator_data["PossibleUnits"].split("; ")
    
#     if len(possible_units) > 1:
#         unit_text = 'Select the data unit:'
#         unit_label = QLabel(unit_text)
#         unit_layout.addWidget(unit_label)
        
#         model = QSqlTableModel(db = AnswersDatabase)
#         model.setTable("IndicatorsSetup")
#         model.select()
        
#         unit_combo_box = QComboBox()
#         unit_combo_box.addItems(possible_units)
#         # Find the corresponding unit in the model
#         model_column_name = "IndicatorUnit"
#         model_row = find_model_row(model, 'IndicatorID', IndicatorID)
        
#         if model_row >= 0:
#             # Get the unit value from the model
#             initial_unit_value = model.data(model.index(model_row, model.fieldIndex(model_column_name)))
#             if initial_unit_value in possible_units:
#                 initial_index = possible_units.index(initial_unit_value)
#                 unit_combo_box.setCurrentIndex(initial_index)
#             else:
#                 update_model(0, IndicatorID, unit_combo_box, model)

#         unit_combo_box.currentIndexChanged.connect(lambda index: update_model(index, IndicatorID, unit_combo_box, model))
#         unit_layout.addWidget(unit_combo_box)
        
#     else:
#         unit_text = f'Data unit: {possible_units[0]}'
#         unit_label = QLabel(unit_text)
#         unit_layout.addWidget(unit_label)   
            
#     if IndicatorID in ["P1", "P2", "V1"]:
#         pass
#     elif IndicatorID in ["B1"]:
#         pass
#     elif IndicatorID in ["SRP1", "SRP2", "SRP3"]:
#         pass
        
#     return indicator_widget

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
    