template_init = """Based on the user's news history, think step by step and recommend candidate news articles.
# Input
## User's History News
${history}
## Candidate News
${candidate}
# Output Format
Rank candidate news based on the user's history news in the format: "Ranked news: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>"."""

template_init_4 = """Based on the user's news history, recommend candidate news articles.
# Input
## User's History News
${history}
## Candidate News
${candidate}
# Output Format
Rank candidate news and start with the phrase in the format: "Ranked news: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>"."""

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

template_final_4 = """# Input:
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
- Rank candidate news based on the user's history news and start with the phrase in the format: "Ranked news: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>".
- Focusing on the alignment of topics rather than the original order of 'Candidate News'.
- The model must also summarize the user's interests and explain the recommendation results.
- Output the ranked list first and then explain the results.
"""

template_best_5191 = """Based on the user's news history, analyze and recommend candidate news articles that align with the user's interests. The recommendation should be made solely based on the semantic relevance of the candidate news to the user's interests, without being influenced by the order of appearance in the 'Candidate News' list.

# Task Description
The task is to recommend news articles to a user based on their history of news interactions. 'User's History News' consists of articles the user has previously shown interest in, while 'Candidate News' includes potential articles of interest. The goal is to identify and rank the candidate news articles that are most relevant to the user's interests.

# Recommendation Process
1. Analyze 'User's History News' to extract keywords and summarize the user's interests into topics.
2. Group semantically similar keywords to form a "Topic" representing a concept of interest to the user.
3. Extract keywords from 'Candidate News' and evaluate how well they match the user's topics of interest.
4. Rank the candidate news based on the strength of the semantic match to the user's interests, disregarding the order in which they appear in 'Candidate News'.

# Input
## User's History News
${history}
## Candidate News
${candidate}

# Output Format
Summarize the user's interests and rank the candidate news according to their relevance to these interests. Provide a justification for the ranking and explain the recommendation results. The output should be in the following format: "Candidate news ranked solely by relevance to the user's interests: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>".

"""

template_best_4812 = """## Task Description
The news recommendation task involves analyzing the user's history news and recommending candidate news articles solely based on the user's interests. 'User's History News' represents the news the user has interacted with previously, and 'Candidate News' represents news the user may be interested in. The recommendation should solely rely on the user's interests, not the order in which the news appears in 'Candidate News'. This task selects the news most relevant to the user's interests.

## Recommendation Process
The recommendation process begins with analyzing and summarizing the user's interests. Keywords are extracted from 'User's History News' and then grouped by meaning, with semantically similar words representing related concepts called a "Topic". These keywords can summarize and infer topics the user is interested in. Then, keywords are extracted from 'Candidate News' and analyzed to determine how well the keywords extracted from each Candidate News match the user's topics of interest. It is emphasized that the recommendation should not be affected by the position of the news in the 'Candidate News' but only by the matching relationship between the candidate news and the user's interests.

## Input
### User's History News
${history}
### Candidate News
${candidate}

## Output Format
Summarize the user's interest and rank candidate news according to their relevance to the user's interest in the format: "Candidate news ranked solely by relevance to the user's interests: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>". The model must also summarize the user's interests and explain the recommendation results.
"""

template_best_4898_2 = """## Task Description
The news recommendation task involves analyzing the user's history news and recommending candidate news articles solely based on the user's interests. 'User's History News' represents the news the user has interacted with previously, and 'Candidate News' represents news the user may be interested in. The recommendation should solely rely on the user's interests, not the order in which the news appears in 'Candidate News'. This task selects the news most relevant to the user's interests.

## Input
### User's History News
${history}
### Candidate News
${candidate}

## Recommendation Process
The recommendation process involves the following steps:
1. Analyzing and summarizing the user's interests: Keywords are extracted from 'User's History News' and then grouped by meaning, with semantically similar words representing related concepts called a "Topic". These keywords can summarize and infer topics the user is interested in.
2. Extracting keywords from 'Candidate News': Keywords are extracted from 'Candidate News' and analyzed to determine how well they match the user's topics of interest. The recommendation should not be affected by the position of the news in the 'Candidate News' but only by the matching relationship between the candidate news and the user's interests.

## Output Format
Summarize the user's interest and rank candidate news according to their relevance to the user's interest in the format: "Candidate news ranked solely by relevance to the user's interests: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>". The model must also summarize the user's interests and explain the recommendation results.
"""
template_best_4898_7 = """# Task Description
The news recommendation task involves analyzing the user's history news and recommending candidate news articles based solely on the user's interests. 'User's History News' represents the news the user has interacted with previously, and 'Candidate News' represents news the user may be interested in. The recommendation should solely rely on the user's interests, not the order in which the news appears in 'Candidate News'. This task selects the news most relevant to the user's interests.

## Recommendation Process
1. Analyze and summarize the user's interests: Extract keywords from 'User's History News' and group them by meaning, with semantically similar words representing related concepts called a "Topic". These keywords can summarize and infer topics the user is interested in.
2. Extract keywords from 'Candidate News': Analyze how well the keywords extracted from each Candidate News match the user's topics of interest. The recommendation should not be affected by the position of the news in the 'Candidate News' but only by the matching relationship between the candidate news and the user's interests.

## Input
### User's History News
${history}
### Candidate News
${candidate}

## Output Format
Summarize the user's interest and rank candidate news according to their relevance to the user's interest in the format: "Candidate news ranked solely by relevance to the user's interests: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>". The model must also summarize the user's interests and explain the recommendation results.

"""
template_best_503 = """## Task Description
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
template_best_5037 = """
Based on the user's news history, think step by step and recommend candidate news articles that align with the user's interests.

# Task Description
The goal is to analyze the 'User's History News' to understand the user's past interests and then recommend 'Candidate News' that the user may find engaging. The recommendation should be based solely on the semantic relevance to the user's interests, not the order in which the news appears in 'Candidate News'. The task is to select news articles that are most relevant to the user's interests as demonstrated by their news history.

# Recommendation Process
1. Analyze 'User's History News' to extract keywords and summarize the user's interests.
2. Group keywords by meaning to form "Topics" that represent related concepts the user is interested in.
3. Extract keywords from 'Candidate News' and evaluate how well they match the user's topics of interest.
4. Rank the 'Candidate News' based on the semantic relevance to the user's interests, disregarding the position of the news in the list.

# Input
## User's History News
${history}
## Candidate News
${candidate}

# Output Format
Summarize the user's interests and rank the candidate news according to their relevance to the user's interests in the format: "Candidate news ranked solely by relevance to the user's interests: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>". Provide an explanation for the ranking and the relevance of each selected candidate news article to the user's interests.

"""
template_best_5037_4 = """
Based on the user's news history, recommend candidate news articles that align with the user's interests.

# Task Description
The goal is to analyze the 'User's History News' to understand the user's past interests and then recommend 'Candidate News' that the user may find engaging. The recommendation should be based solely on the semantic relevance to the user's interests, not the order in which the news appears in 'Candidate News'. The task is to select news articles that are most relevant to the user's interests as demonstrated by their news history.

# Recommendation Process
1. Analyze 'User's History News' to extract keywords and summarize the user's interests.
2. Group keywords by meaning to form "Topics" that represent related concepts the user is interested in.
3. Extract keywords from 'Candidate News' and evaluate how well they match the user's topics of interest.
4. Rank the 'Candidate News' based on the semantic relevance to the user's interests, disregarding the position of the news in the list.

# Input
## User's History News
${history}
## Candidate News
${candidate}

# Output Format
Summarize the user's interests and rank the candidate news according to their relevance to the user's interests start with the phrase in the format: "Candidate news ranked solely by relevance to the user's interests: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>". Provide an explanation for the ranking and the relevance of each selected candidate news article to the user's interests.
Output the ranked list first and then explain the results.
"""
template_best_5074 = """Based on the user's news history, analyze and recommend candidate news articles that align with the user's interests. The recommendation should be made solely based on the semantic relevance of the user's interests to the candidate news.

# Task Description
The goal is to recommend news articles to a user based on their history of news interactions. 'User's History News' consists of articles the user has previously shown interest in, while 'Candidate News' includes potential articles the user may find engaging. The recommendation must focus on the semantic alignment between the user's interests and the candidate news, disregarding the order in which the candidate news is presented.

# Recommendation Process
1. Analyze 'User's History News' to extract and summarize the user's interests into topics.
2. Group semantically similar keywords from the user's history into "Topics" that represent the user's areas of interest.
3. Extract keywords from 'Candidate News' and evaluate how well they semantically match the user's topics of interest.
4. Ensure that the recommendation is not influenced by the sequence of 'Candidate News' but solely by the semantic relevance to the user's interests.

# Input
## User's History News
${history}
## Candidate News
${candidate}

# Output Format
Summarize the user's interests and rank candidate news according to their relevance to the user's interests. Provide an explanation for the ranking and relevance of each candidate news to the user's interests. Use the following format for the recommendation results:

"Candidate news ranked solely by relevance to the user's interests: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>"

"""
template_best_5167 = """## Task Description
This task involves recommending news articles to the user based on their history news and interests. 'User's History News' represents the news the user has interacted with previously, and 'Candidate News' represents news the user may be interested in. The recommendation should solely rely on the user's interests, not on the order in which the news appears in 'Candidate News'. The goal is to select the news most relevant to the user's interests.

## Input
### User's History News
${history}
### Candidate News
${candidate}

## Recommendation Process
The recommendation process involves several steps:
1. Analyze and summarize the user's interests: Extract keywords from 'User's History News' and group them by meaning, with semantically similar words representing related concepts called a "Topic". These keywords can summarize and infer topics the user is interested in.
2. Extract keywords from 'Candidate News': Analyze how well the keywords extracted from each Candidate News match the user's topics of interest. Again, it is emphasized that the recommendation should not be affected by the position of the news in the 'Candidate News', but only by the matching relationship between the candidate news and the user's interests.

## Output Format
Summarize the user's interest and rank candidate news according to their relevance to the user's interest in the format: "Candidate news ranked solely by relevance to the user's interests: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>". The model must also summarize the user's interests and explain the recommendation results.
"""
