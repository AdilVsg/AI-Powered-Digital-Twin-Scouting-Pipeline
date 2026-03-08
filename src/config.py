DEFINITION_DIGITAL_TWIN = '''

A Digital Twin is, by definition, an organized set of digital models representing a real-world entity (such as an industrial machine, a vehicle, or a building) to meet specific monitoring or optimization needs. Unlike simple Computer-Aided Design (CAD), which remains static once the drawing is finished, the Digital Twin is a living and dynamic system. Its fundamental characteristic is its ability to be updated with reality, with a frequency and precision adapted to its use. It does not live in isolation: it exists thanks to a constant data flow from the physical object via technologies like the Internet of Things (IoT) and Big Data.

It is crucial to understand that the term "Digital Twin" is often misused to describe three very different levels of technological maturity, illustrated in your source document:

Level 1: The Digital Model: This is the most basic level. It is a digital representation of a physical object (e.g., a 3D blueprint of an engine), but without any automated connection. Data must be entered manually to update the model. If you find a GitHub repo that only contains static 3D files without network connection code, it is a Model, not a Twin.

Level 2: The Digital Shadow: This is a very common intermediate level. Here, there is an automated information flow, but it is unidirectional (from physical to virtual). The real object sends sensor data to the computer to visualize its state in real-time (monitoring). The computer "sees" what is happening but cannot directly act back on the object.

Level 3: The Digital Twin in the strict sense: This is the most advanced level and the actual target of the industry of the future. It is distinguished by a bidirectional automated information flow. Not only does the system receive data from the real world to analyze and predict failures (predictive maintenance), but it is also capable of sending commands back to the physical object to optimize its operation or correct a defect, thus closing the control loop.

A Digital Twin is therefore a level 3 project.

'''

INSTRUCTIONS = f'''
You are a binary classifier.

Decide if the project described below is a STRICT Digital Twin (level 3 only).

Strict definition:
{DEFINITION_DIGITAL_TWIN}

ABSOLUTE Rules:
- Answer ONLY with <yes> or <no>
- No other text
- No justification

README:
'''

# Choose model - uncomment the one you want to use
# MODEL_ID = "google/gemma-2b-it"  # For low VRAM (< 6GB) CPU only friendly
# MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"  # For medium VRAM (8-16GB): ~14GB VRAM Very slow in CPU only
# MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct" # For high VRAM (>24GB) NEED GPU
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

TRUST_REMOTE_CODE = True

import torch
# Check GPU availability
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    DEVICE_MAP = 'auto'
else:
    print('Running on CPU')
    DEVICE_MAP = 'cpu'