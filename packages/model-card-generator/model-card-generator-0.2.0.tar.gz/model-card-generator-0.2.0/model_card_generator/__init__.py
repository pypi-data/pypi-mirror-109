from .env import *
from .model_data import *
from .pdf_writer import *
from .json_writer import *

mc = ModelData(
    get_env('model_name'), 
    get_env('model_date'), 
    get_env('model_version'),

    get_env('dataset_aroeira_images'),
    get_env('dataset_capororoca_images'),
    get_env('dataset_embauba_images'),
    get_env('dataset_jeriva_images'),
    get_env('dataset_mulungu_images'),
    get_env('dataset_pitangueira_images'),
    get_env('dataset_total_images'),
    get_env('dataset_labeler_name'),
    get_env('dataset_augmentation_type'),
    get_env('dataset_augmentation_size'),
    get_env('dataset_batch_size'),
    get_env('dataset_validation_percentage'),

    get_env('tl_has_trained'),
    get_env('tl_model'),
    get_env('tl_epochs'),
    get_env('tl_learning_rate'),

    get_env('ft_has_unfreezed'),
    get_env('ft_has_trained'),
    get_env('ft_epochs'),
    get_env('ft_learning_rate_floor'),
    get_env('ft_learning_rate_ceiling')
)
