import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import BitsAndBytesConfig
device = "cuda"

tokenizer = AutoTokenizer.from_pretrained("D:\\model\\glm-4v-9b", trust_remote_code=True)

query = '识别该图像中的表格信息，并通过html格式输出'
image = Image.open("table.png").convert('RGB')
inputs = tokenizer.apply_chat_template([{"role": "user", "image": image, "content": query}],
                                       add_generation_prompt=True, tokenize=True, return_tensors="pt",
                                       return_dict=True)  # chat mode
nf4_config = BitsAndBytesConfig(
   load_in_4bit=True,
   bnb_4bit_quant_type="nf4",
   bnb_4bit_use_double_quant=True,
   bnb_4bit_compute_dtype=torch.bfloat16
)
inputs = inputs.to(device)
model = AutoModelForCausalLM.from_pretrained(
    "D:\\model\\glm-4v-9b",
    quantization_config=nf4_config,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    trust_remote_code=True
).eval()

gen_kwargs = {"max_length": 2500, "do_sample": True, "top_k": 1}
with torch.no_grad():
    outputs = model.generate(**inputs, **gen_kwargs)
    outputs = outputs[:, inputs['input_ids'].shape[1]:]
    print(tokenizer.decode(outputs[0]))