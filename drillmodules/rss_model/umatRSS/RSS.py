"""
RSS module

Defines the RSS class
"""


class RSS:
    """
    RSS model

    Defines the an RSS system for sumulation

    Parameters:
        - __targets: Private array of targets to hit. Targets can be added
                    through self.addTarget
        - survey_instance: A class instance with well path data for surveying
        - start_coordinates: Start coordinates. Default is [0,0,0]
        - kop: Kick off point

    """
    __targets = []

    survey_instance = None

    start_coordinates = [0,0,0]
    kop = None
    
    # Other Parameters

    def takeSurvey(self):
        """Takes survey using self.survey_instance"""
        pass
    
    def addTarget(self, coords):
        """
        Add a target to the RSS.
        Target must be in an array form (target_inclination, target_azimuth)
        """

        # Parses a target and an places it in the right accesending index of
        # the RSS targets array

    def start(self):
        """Starts the simulation"""
        
        # Begin Simulation

