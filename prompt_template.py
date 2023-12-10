template_init = """Based on the user's news history, think step by step and recommend candidate news articles.
# Input
## User's History News
${history}
## Candidate News
${candidate}
# Output Format
Rank candidate news based on the user's history news in the format: "Ranked news: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>"."""

template_final = """# Input:
User's History News:
${history}
Candidate News:
${candidate}

# Task Description:
1. 'User's History News' features headlines that have previously engaged the user, signaling their interests.
2. 'Candidate News' presents a set of headlines not yet seen by the user. The sequence of these headlines should not influence the ranking.
3. Your objective is to select the top 10 headlines from 'Candidate News' that most closely resonate with the user's interests as reflected in 'User's History News'.

# Recommendation Process:
1. Independently assess 'User's History News' to deduce the user's core interested topics.
2. Scrutinize the topics of 'Candidate News', disregarding their initial order, to gauge their relevance to the user’s interests.
3. Strategically rank the 'Candidate News' headlines by relevance, not by their original placement in the list.

# Output Format:
- Rank candidate news based on the user's history news in the format: "Ranked news: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>".
- Focusing on the alignment of topics rather than the original order of 'Candidate News'.
- The model must also summarize the user's interests and explain the recommendation results.
"""

template_best = """## Task Description
The goal is to recommend news articles to a user based on their history of news interactions. 'User's History News' represents articles the user has previously shown interest in, while 'Candidate News' comprises potential articles that may align with the user's interests. The recommendation should be made solely on the basis of the user's interests, without being influenced by the sequence of the 'Candidate News'. The task is to identify the news articles most relevant to the user's interests.

## Recommendation Process
1. Analyze 'User's History News' to identify and summarize the user's interests. Extract keywords and group them by meaning to form "Topics" that represent the user's areas of interest.
2. Extract keywords from 'Candidate News' and evaluate how well they align with the user's "Topics" of interest.
3. Ensure that the recommendation is not biased by the order of the 'Candidate News' but is solely based on the relevance of each candidate article to the user's interests.

## Input
### User's History News
${history}
### Candidate News
${candidate}

## Output Format
Summarize the user's interests and rank the candidate news according to their relevance to these interests. Provide a ranked list in the format: "Candidate news ranked solely by relevance to the user's interests: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>". Additionally, include a summary of the user's interests and a brief explanation of the ranking rationale for the top recommended articles.
"""

# template_best = """## Task Description
# This task involves recommending news articles to the user based on their history news and interests. 'User's History News' represents the news the user has interacted with previously, and 'Candidate News' represents news the user may be interested in. The recommendation should solely rely on the user's interests, not on the order in which the news appears in 'Candidate News'. The goal is to select the news most relevant to the user's interests.
#
# ## Input
# ### User's History News
# ${history}
# ### Candidate News
# ${candidate}
#
# ## Recommendation Process
# The recommendation process involves several steps:
# 1. Analyze and summarize the user's interests: Extract keywords from 'User's History News' and group them by meaning, with semantically similar words representing related concepts called a "Topic". These keywords can summarize and infer topics the user is interested in.
# 2. Extract keywords from 'Candidate News': Analyze how well the keywords extracted from each Candidate News match the user's topics of interest. Again, it is emphasized that the recommendation should not be affected by the position of the news in the 'Candidate News', but only by the matching relationship between the candidate news and the user's interests.
#
# ## Output Format
# Summarize the user's interest and rank candidate news according to their relevance to the user's interest in the format: "Candidate news ranked solely by relevance to the user's interests: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>". The model must also summarize the user's interests and explain the recommendation results.
# """