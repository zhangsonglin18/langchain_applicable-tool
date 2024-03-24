import json
import json5
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig

import torch

quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    # bnb_4bit_quant_type='nf4',
    # bnb_4bit_compute_dtype=torch.bfloat16
)


# model = AutoModelForCausalLM.from_pretrained(
#     "Qwen1.5-1.8B-Chat_fine",
#     device_map=device
# )
# tokenizer = AutoTokenizer.from_pretrained("Qwen1.5-1.8B-Chat_fine")

tokenizer = AutoTokenizer.from_pretrained("D:\\model\\Qwen1.5-1.8B-Chat", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("D:\\model\\Qwen1.5-1.8B-Chat",
                                         quantization_config = quantization_config,
                                         device_map="auto",
                                         trust_remote_code=True)
