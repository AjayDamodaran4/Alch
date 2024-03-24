from .bodySite import bodySite
from .Laterality import Laterality
from .probability import Probability_Qualifier
from .presence_qualifier import Presence_Qualifier
from .obs_code import ObservationCode
from .obs_display import ObservationDisplay
from .study_UID import Study_Identifier
from .Tracking_ID_UID import Tracking_Identifier
from .observation_code import Observation_Code_Display
from .Tracking import Tracking_ID

__all__ = [
    'bodySite',
    'Laterality',
    'Probability_Qualifier',
    'Presence_Qualifier',
    'ObservationCode',
    'ObservationDisplay',
    'Study_Identifier',
    'Tracking_Identifier',
    'Observation_Code_Display',
    'Tracking_ID'
]


class FhirUtils(bodySite,Laterality, Probability_Qualifier, Presence_Qualifier, ObservationCode,ObservationDisplay,Study_Identifier,Tracking_Identifier, Observation_Code_Display,Tracking_ID):
    def __init__(self):
        # Call the __init__ method of each parent class explicitly
        bodySite.__init__(self)
        Laterality.__init__(self)
        Probability_Qualifier.__init__(self)
        Presence_Qualifier.__init__(self)
        ObservationCode.__init__(self)
        ObservationDisplay.__init__(self)
        Study_Identifier.__init__(self)
        Tracking_Identifier.__init__(self)
        Observation_Code_Display.__init__(self)
        Tracking_ID.__init__(self)