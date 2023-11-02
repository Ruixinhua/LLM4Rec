template1 = """{{#system~}}
You serve as a personalized news recommendation system.
{{~/system}}

{{#user~}}
# Input:
User's History News:
{{history}}
Candidate News:
{{candidate}}

# Task Description:
1. 'User's History News' encompasses headlines that have previously engaged users, reflecting their interests. 
2. 'Candidate News' contains potential headlines yet to be presented to the user. 
3. Select the top 10 most relevant headlines from 'Candidate News' that align with the user's demonstrated preference. 

# Recommendation Process:
1. Analyze 'User's History News' to distill the user's preferred topics;
2. Determine the topics of the candidate news and cross-examine them with the user’s interests;
3. Prioritize 'Candidate News' by the degree of topic overlap with the user’s interests.
#Output Guidelines:
1. Rank the top 10 headlines from 'Candidate News', and first output the list formatted as: 'C#,C#,C#,C#,C#,C#,C#,C#,C#,C#'.
2. Provide a succinct summary of the key topics for each headline.
3. Highlight the connection between these topics and the user's interests identified in 'User's History News'.
4. Keep the overall output within a 200-word limit.
{{~/user}}

{{#assistant~}}
{{gen 'rank' temperature=${temperature} max_tokens=200}}
{{~/assistant}}
"""

template2 = """{{#system~}}
You serve as a personalized news recommendation system.
{{~/system}}

{{#user~}}
# Input:
User's History News:
{{history}}
Candidate News:
{{candidate}}

# Task Description:
1. 'User's History News' contains headlines that have captured the user's attention previously, indicating their areas of interest.
2. 'Candidate News' comprises headlines that the user has not yet seen but may find interesting.
3. Your goal is to select the top 10 headlines from 'Candidate News' that best match the user's interests as shown in 'User's History News'.

# Recommendation Process:
1. Extract and list the main topics from 'User's History News'.
2. Identify the themes within 'Candidate News' and compare them to the user’s listed interests.
3. Rank the 'Candidate News' headlines based on how closely they align with the user's interests.

# Output Format:
- Begin with a statement like "The top 10 recommended news headlines are: C#,C#,C#,C#,C#,C#,C#,C#,C#,C#."
- Follow with a ranked explanation for each headline, starting with the highest priority, in the format "C# is ranked first because it shares topics A, B, and C with the user's history."
- Continue this format down the list for each of the top 10 headlines.
- Ensure that the entire output remains within a 200-word limit.

{{~/user}}

{{#assistant~}}
{{gen 'rank' temperature=${temperature} max_tokens=200}}
{{~/assistant}}
"""

template3 = """{{#system~}}
You serve as a personalized news recommendation system.
{{~/system}}

{{#user~}}
# Input:
User's History News:
{{history}}
Candidate News:
{{candidate}}

# Task Description:
1. 'User's History News' contains headlines that have captured the user's attention previously, indicating their areas of interest.
2. 'Candidate News' contains potential headlines yet to be presented to the user. Don't affect by the order of the candidate news. 
3. Your goal is to select the top 10 headlines from 'Candidate News' that best match the user's interests as shown in 'User's History News'.

# Recommendation Process:
1. Extract and analysis the main topics from 'User's History News'.
2. Identify the topics within 'Candidate News' and compare them to the user’s listed interests.
3. Rank the 'Candidate News' headlines based on how closely they align with the user's interests.

# Output Format:
- Begin with a statement like "The top 10 recommended news headlines are: C#,C#,C#,C#,C#,C#,C#,C#,C#,C#."
- Follow with a ranked explanation for each headline, starting with the highest priority, in the format "Topic of C# is about #Topics, which shares with the user's history H#(,H#, and H#)."
- Continue this format down the list for each of the top 10 headlines.
- Ensure that the entire output remains within a 200-word limit.
{{~/user}}

{{#assistant~}}
{{gen 'rank' temperature=${temperature} max_tokens=200}}
{{~/assistant}}
"""

template4 = """{{#system~}}
You serve as a personalized news recommendation system.
{{~/system}}

{{#user~}}
# Input:
User's History News:
{{history}}
Candidate News:
{{candidate}}

# Task Description:
1. 'User's History News' features headlines that have previously engaged the user, signaling their interests.
2. 'Candidate News' presents a set of headlines not yet seen by the user. The sequence of these headlines should not influence the ranking.
3. Your objective is to impartially select the top 10 headlines from 'Candidate News' that most closely resonate with the user's interests as reflected in 'User's History News'.

# Recommendation Process:
1. Independently assess 'User's History News' to deduce the user's core interested topics.
2. Scrutinize the topics of 'Candidate News', disregarding their initial order, to gauge their relevance to the user’s interests.
3. Strategically rank the 'Candidate News' headlines by relevance, not by their original placement in the list.

# Output Format:
- Start with the phrase: "The top 10 recommended news headlines, ranked solely by relevance to the user's interests, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
- Proceed with a relevance-based justification for each headline's ranking, such as: "C# pertains to topics X, Y, Z, which align with the user's interest shown in headlines H#, H#, H#."
- Maintain this structure for each of the top 10 headlines.
- The total output should not exceed a 200-word limit, focusing on the alignment of topics rather than the original order of 'Candidate News'.
{{~/user}}

{{#assistant~}}
{{gen 'rank' temperature=${temperature} max_tokens=200}}
{{~/assistant}}
"""