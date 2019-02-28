# ----------------------------
#  Andrea Silvestroni 2019
#  Residual Noise Extraction and Smartphone Linking
#
#  A number of constants used throughout the project
# ----------------------------

sizes = dict(width=1024, height=1024)

session_statuses = {
    'error':   'error',
    'wait':    'waiting',
    'gather':  'gathering',
    'process': 'processing',
    'cluster': 'clustering',
    'done':    'completed'
    }

picture_statuses = {
    'invalid_size':  'invalid size',
    'invalid_noise': 'invalid_noise',
    'wait':          'waiting',
    'preprocessing': 'preprocessing',
    'preprocessed':  'preprocessed',
    'extracting':    'extracting',
    'extracted':     'extracted',
    'done':          'completed'
    }
status_invalid_size = 'invalid size'
result_invalid_noise = 'invalid noise'
status_extracted = 'extracted'
status_preprocessed = 'preprocessed'
status_extracting = 'extracting'
status_preprocessing = 'preprocessing'

thumbnail_sizes = (400, 400)

fb_max_pictures = 40
