gpt_template = """{{#system~}}
${system_instruction}
{{~/system}}

{{#user~}}
${prompt_temp}
{{~/user}}

{{#assistant~}}
{{gen 'output' temperature=${temperature} max_tokens=${max_tokens} seed=${seed}}}
{{~/assistant}}
"""

llama_template = """${system_instruction}
${prompt_temp}
{{gen 'output' do_sample=False max_tokens=${max_tokens}}}"""

sys_instruction = "You serve as a personalized news recommendation system."


sys_instruction_format = """You serve as a personalized news recommendation system. You should first output the ranked list and then provide explanations. The explanations should accurately and comprehensively summarize the user's interests. Then, the explanations should categorize each candidate news item into related topics and explain its relevance to the user's interests."""
