import json
from .model_data import ModelData 

assessment_filename='assessment.json'

def write_json(model_data: ModelData): 
    """Writes assessment JSON file"""
    
    with open(assessment_filename, 'w') as outfile:
        json.dump(model_data, 
            outfile,
            default=lambda o: o.__dict__,  
            indent=4, 
            ensure_ascii=False)