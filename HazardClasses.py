from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

class ClassHazards:
    def __init__(self, ClassesValues: list, ValuesType: int, Methodology: str ):
        """_summary_

        Args:
            ClassesValues (list): Provide the hazard values for each class, from the lower to the higer class, i.e, lower hazard to higher hazard.
            ValuesType (int): 1 for percentage, 2 for value
            Methodology (int): Choose methodology to calculate the hazard
            P1: Pedestrian hazard by DEFRA (2005)
            V1: Vehicles hazard by Martinez et al (2017)
        """       
        MethodologyNrClasses = {"P1": 4,
                                "V1": 3}
         
        if ClassesValues is None or ClassesValues == []:
            raise TypeError("ClassHazards: ClassesValues is None, must be a list with values")
        
        if ValuesType != 1 and ValuesType != 2:
            raise TypeError("ClassHazards: ValuesType must be 1 (for %) or 2 (for real)")
        
        if Methodology not in MethodologyNrClasses.keys():
            raise TypeError("ClassHazards: Methodology not available...")
        
        if len(ClassesValues) != MethodologyNrClasses[Methodology] :
            raise TypeError("ClassHazards: Number of class values does not match the number of classes of the methodlogy")
       
        self.values = ClassesValues
        self.methodology = Methodology
        self.datatype = ValuesType
       
        self.ClassesWeights = self.getClassesWeights()
        
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
            classvalue = self.values[index] * self.ClassesWeights[index][1] / denominator   
            Hazard += classvalue
        return round(Hazard, 2)

class BuildingHazard:
    def __init__(self,
                 Methodology: str,
                 UserBuildingUsesOnMethodology: dict,
                 UserBuilingsSize: dict,
                 WaterHeightOnBuildings: dict):
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


if __name__ == '__main__':
    testPed = [732787.76, 57829.44, 115074.42, 1525.20]
    HazardPedestrian = ClassHazards(testPed, 2, 'P1').calculateHazard()
    print(HazardPedestrian)
    testVehic = [80.34, 4.39, 15.26]
    HazardVehicles = ClassHazards(testVehic, 1, 'V1').calculateHazard()
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
    