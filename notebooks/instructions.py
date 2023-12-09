meta_instruction = """You should generate an improved prompt template based on the provided information, which consists of two parts: 
- the current prompt template between "# Current Prompt Template Begin" and "# Current Prompt Template End" and the previous best prompt template between "# Previous Best Prompt Template Begin" and "# Previous Best Prompt Template End".
- some samples with required fields by the prompt template and observation results between "# Sample Begin" and "# Sample End". 
You should provide an enhanced prompt template between "# Prompt Template Begin" and "# Prompt Template End". Use "${history}" as the placeholder for the user's history news and "${candidate}" as the placeholder for the candidate news.
"""
# and a monitor that records the current performance and previous best performance with the corresponding prompt template under "# Monitor". You should provide an enhanced prompt template between "# Prompt Template Begin" and "# Prompt Template End".
guide_instruction_complex = """Generate a better prompt that guides the recommender in making recommendations. The generated prompt must be placed between "# Prompt Template Begin" and "# Prompt Template End" and must include the placeholders "${history}" under "## User's History News" and "${candidate}" under "## Candidate News". Observe the differences between "# Best Prompt Template" and "# Current Prompt Template". If "# Best Prompt Template" and "# Current Prompt Template" are different, analyze why "# Best Prompt Template" is better than "# Current Prompt Template", and on this basis, improve "# Best Prompt Template" to achieve better recommendation results. Do not directly copy sentences from the "# Current Prompt Template" and "# Best Prompt Template". 
"""
guide_instruction_naive = """The generated prompt must be placed between "# Prompt Template Begin" and "# Prompt Template End" and must include the placeholders "${history}" under "## User's History News" and "${candidate}" under "## Candidate News".
"""
non_repeat = """Don't directly copy and paste the "# Current Prompt Template" and "# Best Prompt Template" as the generated prompt."""

naive_prompt_temp = """# Input:
## User's History News:
${history}
## Candidate News:
${candidate}
# Output Format:
Rank candidate news based on the user's history news in the format: "Ranked news: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>"."""
naive_prompt_zero_shot = """Based on the user's news history, think step by step and recommend candidate news articles.
# Input
## User's History News
${history}
## Candidate News
${candidate}
# Output Format
Rank candidate news based on the user's history news in the format: "Ranked news: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>"."""
initial_prompt = """# Input
## User's History News
${history}
## Candidate News
${candidate}

# Task Description
1. 'User's History News' features headlines that have previously engaged the user, signaling their interests.
2. 'Candidate News' presents a set of headlines not yet seen by the user. The sequence of these headlines should not influence the ranking.
3. Your objective is to impartially select the top 10 headlines from 'Candidate News' that most closely resonate with the user's interests as reflected in 'User's History News'.

# Recommendation Process
1. Independently assess 'User's History News' to deduce the user's core interested topics.
2. Scrutinize the topics of 'Candidate News', disregarding their initial order, to gauge their relevance to the user’s interests.
3. Strategically rank the 'Candidate News' headlines by relevance, not by their original placement in the list.

# Output Format
- Start with the phrase: "The top 10 recommended news headlines, ranked solely by relevance to the user's interests, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
- Proceed with a relevance-based justification for each headline's ranking, such as: "C# pertains to topics X, Y, Z, which align with the user's interest shown in headlines H#, H#, H#."
- Maintain this structure for each of the top 10 headlines.
- The total output should not exceed a 200-word limit, focusing on the alignment of topics rather than the original order of 'Candidate News'."""
prompt_temp = """# Current Prompt Template Begin
${prompt_temp}
# Current Prompt Template End
"""
best_prompt_temp = """# Previous Best Prompt Template Begin
${best_prompt_temp}
# Previous Best Prompt Template End
"""

sample_temp = """# Sample Begin
## Prompt for the Recommender 
${full_prompt}
## Recommender's Answer
${answer}
## User's Click
${click}
# Sample End
"""

observation_instruction_naive = """Focus on the given sample and analyze the content of the prompt for the recommender and the recommender's answer based on the user's click. Observations can focus on the following aspects:
- Whether the recommender's answer correctly extracts the keywords from the user's history news.
- Whether the keywords extracted from the recommender's answer accurately summarise the topics of interest to the user.
- Whether the recommender's answer correctly extracts keywords from the candidate news and correctly matches the user's interests.
You should generate an enhanced prompt template based on the above observations, detailing the task requirements so that the recommender can answer using the guidance given above. Use "${history}" as the placeholder for the "User's History News" and "${candidate}" as the placeholder for the "Candidate News"."""
observation_instruction_complex = """Focus on the given sample and analyze the content of the prompt for the recommender and the recommender's answer based on the user's click. Observations can focus on the following aspects:
- Whether the recommender's answer correctly extracts the keywords from the user's history news.
- Whether the keywords extracted from the recommender's answer accurately summarise the topics of interest to the user.
- Whether the recommender's answer correctly extracts keywords from the candidate news and correctly matches the user's interests.
Based on the observations, you can enhance the prompt by adding a description of the recommendation task, the breakdown of the recommendation process, and the constraints on the final output format so that the recommender can make corresponding recommendations based on semantics only. Here are some suggestions for enhancing the prompt:
- Under "# Input", you can use "${history}" as the placeholder for the user's history news and "${candidate}" as the placeholder for the candidate news.
- Under "# Task Description", you can add a description of the news recommendation task, such as 'User's History News' being the news the user has interacted with previously and 'Candidate News' being news the user may be interested in. The recommendation should solely rely on the user's interests, not the order in which the news appears in 'Candidate News'. This task selects the news most relevant to the user's interests.
- Under "# Recommendation Process", a detailed recommendation process can be added, such as first analyzing and summarizing the user's interests. Keywords are extracted from 'User's History News' and then grouped by meaning, with semantically similar words representing related concepts called a "Topic". These keywords can summarize and infer topics the user is interested in. Then, extract keywords from 'Candidate News' and analyze how well the keywords extracted from each Candidate News match the user's topics of interest. Again, it emphasized that the recommendation should not be affected by the position of the news in the  'Candidate News' but only by the matching relationship between the candidate news and the user's interests.
- Under "# Output Format", define the output format. Summarize the user's interest and rank candidate news according to their relevance to the user's interest in the format:  "Candidate news ranked solely by relevance to the user's interests: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>". The model must also summarize the user's interests and explain the recommendation results.
"""
