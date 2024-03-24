from llm_api.qwen.tools import *
from llm_api.qwen.qwen_model import *
device = "cuda"
def build_planning_prompt(TOOLS, query):
    tool_descs = []
    tool_names = []
    for info in TOOLS:
        tool_descs.append(
            TOOL_DESC.format(
                name_for_model=info['name_for_model'],
                name_for_human=info['name_for_human'],
                description_for_model=info['description_for_model'],
                parameters=json.dumps(
                    info['parameters'], ensure_ascii=False),
            )
        )
        tool_names.append(info['name_for_model'])
    tool_descs = '\\n\\n'.join(tool_descs)
    tool_names = ','.join(tool_names)

    prompt = REACT_PROMPT.format(tool_descs=tool_descs, tool_names=tool_names, query=query)
    return prompt

prompt_1 = build_planning_prompt(TOOLS[0:3], query="中国人口多少")
# print(prompt_1)
# stop = ["Observation:", "Observation:\\n"]
# react_stop_words_tokens = [tokenizer.encode(stop_) for stop_ in stop]
# response_1, _ = model.chat(tokenizer, prompt_1, history=None, stop_words_ids=react_stop_words_tokens)
# print(response_1)
# text = tokenizer.apply_chat_template(
#         prompt_1,
#         tokenize=False,
#         add_generation_prompt=True
#     )
model_inputs = tokenizer([prompt_1], return_tensors="pt").to(device)

generated_ids = model.generate(
    model_inputs.input_ids,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response_1 = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response_1)

from typing import Dict, Tuple


def parse_latest_plugin_call(text: str) -> Tuple[str, str]:
    i = text.rfind('\\nAction:')
    j = text.rfind('\\nAction Input:')
    k = text.rfind('\\nObservation:')
    if 0 <= i < j:  # If the text has `Action` and `Action input`,
        if k < j:  # but does not contain `Observation`,
            # then it is likely that `Observation` is ommited by the LLM,
            # because the output text may have discarded the stop word.
            text = text.rstrip() + '\\nObservation:'  # Add it back.
            k = text.rfind('\\nObservation:')
    if 0 <= i < j < k:
        plugin_name = text[i + len('\\nAction:'):j].strip()
        plugin_args = text[j + len('\\nAction Input:'):k].strip()
        return plugin_name, plugin_args
    return '', ''


def use_api(tools, response):
    use_toolname, action_input = parse_latest_plugin_call(response)
    if use_toolname == "":
        return "no tool founds"

    used_tool_meta = list(filter(lambda x: x["name_for_model"] == use_toolname, tools))
    if len(used_tool_meta) == 0:
        return "no tool founds"

    api_output = used_tool_meta[0]["tool_api"](action_input)
    return api_output


api_output = use_api(TOOLS, response_1)
print(api_output)

prompt_2 = prompt_1 + '\\n' + response_1 + ' ' + api_output
stop = ["Observation:", "Observation:\\n"]

react_stop_words_tokens = [tokenizer.encode(stop_) for stop_ in stop]
# response_2, _ = model.chat(tokenizer, prompt_2, history=None, stop_words_ids=react_stop_words_tokens)
# print(prompt_2, "\\n", response_2)
# text = tokenizer.apply_chat_template(
#         prompt_1,
#         tokenize=False,
#         add_generation_prompt=True
#     )
model_inputs = tokenizer([prompt_2], return_tensors="pt").to(device)

generated_ids = model.generate(
    model_inputs.input_ids,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response_1 = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response_1)