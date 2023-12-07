gpt_template = """{{#system~}}
You serve as a personalized news recommendation system.
{{~/system}}

{{#user~}}
${input}
{{~/user}}

{{#assistant~}}
{{gen 'rank' temperature=${temperature} max_tokens=${max_tokens}}}
{{~/assistant}}
"""

llama_template = """You serve as a personalized news recommendation system.
${input}
{{gen 'rank' do_sample=False max_tokens=200}}"""

template1 = """# Input:
User's History News:
${history}
Candidate News:
${candidate}

# Task Description:
1. 'User's History News' encompasses headlines that have previously engaged users, reflecting their interests. 
2. 'Candidate News' contains potential headlines yet to be presented to the user. 
3. Select the top 10 most relevant headlines from 'Candidate News' that align with the user's demonstrated preference. 

# Recommendation Process:
1. Analyze 'User's History News' to distill the user's preferred topics;
2. Determine the topics of the candidate news and cross-examine them with the user’s interests;
3. Prioritize 'Candidate News' by the degree of topic overlap with the user’s interests.
# Output Guidelines:
1. Rank the top 10 headlines from 'Candidate News', and first output the list formatted as: 'C#,C#,C#,C#,C#,C#,C#,C#,C#,C#'.
2. Provide a succinct summary of the key topics for each headline.
3. Highlight the connection between these topics and the user's interests identified in 'User's History News'.
4. Keep the overall output within a 200-word limit."""

template2 = """# Input:
User's History News:
${history}
Candidate News:
${candidate}

# Task Description:
1. 'User's History News' contains headlines that have captured the user's attention previously, indicating their areas of interest.
2. 'Candidate News' comprises headlines that the user has not yet seen but may find interesting.
3. Your goal is to select the top 10 headlines from 'Candidate News' that best match the user's interests as shown in 'User's History News'.

# Recommendation Process:
1. Extract and list the main topics from 'User's History News'.
2. Identify the topic within 'Candidate News' and compare them to the user’s listed interests.
3. Rank the 'Candidate News' headlines based on how closely they align with the user's interests.

# Output Format:
- Begin with a statement like "The top 10 recommended news headlines are: C#,C#,C#,C#,C#,C#,C#,C#,C#,C#."
- Follow with a ranked explanation for each headline, starting with the highest priority, in the format "C# is ranked first because it shares topics A, B, and C with the user's history."
- Continue this format down the list for each of the top 10 headlines.
- Ensure that the entire output remains within a 200-word limit."""

template3 = """# Input:
User's History News:
${history}
Candidate News:
${candidate}

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
- Ensure that the entire output remains within a 200-word limit."""

template4 = """# Input:
User's History News:
${history}
Candidate News:
${candidate}

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
- The total output should not exceed a 200-word limit, focusing on the alignment of topics rather than the original order of 'Candidate News'."""

template5 = """I want you to act as a personalized news recommendation system. News recommendation involves two main types of data: 'USER'S HISTORY NEWS', which includes news headlines previously clicked by a user, sorted by the time of click, with earlier clicks appearing first; and 'CANDIDATE NEWS', which are the potential news headlines waiting to be recommended. The recommendation process entails summarizing users' preferences and interests based on their historical clicks, then filtering and ranking candidate news according to how well they match these preferences and interests, with higher relevance leading to higher ranking. I will give you the INPUT first as follows:
# INPUT BEGIN
USER'S HISTORY NEWS BEGIN
${history}
USER'S HISTORY NEWS END
CANDIDATE NEWS BEGIN
${candidate}
CANDIDATE NEWS END
# INPUT END
# Recommendation Process:
1. Extract Keywords from News Content: Begin by extracting keywords that accurately describe and represent each news item. These keywords should capture the essence of the news content.
2. Analyze User's History News:
2.1 Extract a collection of keywords from all 'User's History News'.
2.2 Group these keywords into clusters representing related concepts or meanings, known as 'topic'. A topic typically consists of a series of frequently co-occurring words reflecting underlying topics or discussions. For example, a cluster including words like 'NBA', 'player', and 'match' closely relates to the concept of 'sports'. If a user's historical browsing news frequently involves these words, it can be inferred that they are interested in 'sports'.
2.3 The aim here is to analyze the keyword collection to summarize and infer topics that the user is interested in.
3. Match Candidate News with User's Interests.
3.1 Extract keywords from each 'Candidate News'.
3.2 Analyze how well the keywords in each Candidate News match with the user's interested topics.
3.3 The degree of match is defined by how closely the keywords in a candidate news item relate to the corresponding topic. For example, if a user is interested in 'sports' and a candidate news item mentions words like 'NBA' and 'player' it can be considered a perfect match for the user's interest, potentially scoring 10 out of 10 in an assessment scale. Conversely, if a candidate news item focuses on topics like 'dog' and 'cat' related to 'pets' it would not match the user's interest in 'sports' and would rank lower in the recommendation list.
# Output Format:
The output should start with the phrase: "Here are the top 10 recommended news headlines, ranked solely by relevance to the user's interested topics. " and then be followed by the content formatted as "Here are user's interested topics and their related keyword collections: #topic1: #keyword1,#keyword2,etc;#topic2: #keyword1,keyword2,etc; The recommended news headlines by rank are: 
1. #news. The extracted keywords of this news is: #keyword1,#keyword2,etc. The matched topics are: #topic1,#topic2,etc.
...
10. #news. The extracted keywords of this news is: #keyword1,#keyword2,etc. There is no matched topic."
Please replace '#topic1' and '#topic2' with specific topics, '#keyword1' and '#keyword2' with specific keywords, and '#news' with the headlines of correspondingly ranked news. 'etc' indicates there exists zero or more results. The number of topics the user is interested in, the number of keywords, and the number of matched topics should be determined by specific cases. If no matching topic is found in the user's interests for a candidate news headline, then output 'There is no matched topic.' as the result. The ranked news '#news' should only be selected from 'CANDIDATE NEWS'.
# Here is your output:
"""

template6 = """I want you to act as a personalized news recommendation system. News recommendation involves two main types of data: 'USER'S HISTORY NEWS', which includes news headlines previously clicked by a user, sorted by the time of click, with earlier clicks appearing first; and 'CANDIDATE NEWS', which are the potential news headlines waiting to be recommended. The recommendation process entails summarizing users' preferences and interests based on their historical clicks, then filtering and ranking candidate news according to how well they match these preferences and interests, with higher relevance leading to higher ranking. I will give you the INPUT as follows:
# INPUT
USER'S HISTORY NEWS BEGIN
${history}
USER'S HISTORY NEWS END
CANDIDATE NEWS BEGIN
${candidate}
CANDIDATE NEWS END
# Recommendation Process:
1. Extract Keywords from News Content: Begin by extracting keywords that accurately describe and represent each news item. These keywords should capture the essence of the news content.
2. Analyze User's History News:
2.1 Extract a collection of keywords from all 'User's History News'.
2.2 Group these keywords into clusters representing related concepts or meanings, known as 'topic'. A topic typically consists of a series of frequently co-occurring words reflecting underlying topics or discussions. For example, a cluster including words like 'NBA', 'player', and 'match' closely relates to the concept of 'sports'. If a user's historical browsing news frequently involves these words, it can be inferred that they are interested in 'sports'.
2.3 The aim here is to analyze the keyword collection to summarize and infer topics that the user is interested in.
3. Match Candidate News with User's Interests.
3.1 Extract keywords from each 'Candidate News'.
3.2 Analyze how well the keywords in each Candidate News match with the user's interested topics.
3.3 The degree of match is defined by how closely the keywords in a candidate news item relate to the corresponding topic. For example, if a user is interested in 'sports' and a candidate news item mentions words like 'NBA' and 'player' it can be considered a perfect match for the user's interest, potentially scoring 10 out of 10 in an assessment scale. Conversely, if a candidate news item focuses on topics like 'dog' and 'cat' related to 'pets' it would not match the user's interest in 'sports' and would rank lower in the recommendation list.
# Output Format:
- The first sentence of the output should be: "Here are the top 10 recommended news headlines, ranked solely by relevance to the user's interested topics. " 
- The second sentence of the output should summarize the user's interested topics, starting with "Here are user's interested topics and their related keyword collections: ...". This sentence should include all topics that the user is interested in and corresponding keywords.
- The rest of the output should start with "The recommended news headlines by rank are: ...". This part should output up to 10 news from CANDIDATE NEWS set which in the format of "#news: The extracted keywords of this news is: #keyword1,#keyword2,etc. The matched topics are: #topic1,#topic2,etc.", where '#news' is news headline, '#keyword1' and '#keyword2' are corresponding keywords extracted from the headline, and '#topic1' and '#topic2' are specific topics that the user is interested in. If no topic is found, output 'There is no matched topic.' as the result.
# VERY IMPORTANT
DON'T let the sequence order of the 'CANDIDATE NEWS' influence you.
DON'T let the sequence order of the 'CANDIDATE NEWS' influence you.
DON'T let the sequence order of the 'CANDIDATE NEWS' influence you.
# Here is your output:
"""

template7 = """News recommendation involves two main types of data: 'USER'S HISTORY NEWS', which includes news headlines previously clicked by a user, sorted by the time of click, with earlier clicks appearing first, and 'CANDIDATE NEWS', which are the potential news headlines waiting to be recommended. The recommendation process entails summarizing users' preferences and interests based on their historical clicks, then filtering and ranking candidate news according to how well they match these preferences and interests, with higher relevance leading to higher ranking. The format of 'USER'S HISTORY NEWS' is in 'H#: #news', where 'H#' is the ID of the news and '#news' contains the news headline. The format of 'CANDIDATE NEWS' is in 'C#: #news', where 'C#' is the ID of the news and '#news' contains the news headline.
# INPUT
USER'S HISTORY NEWS BEGIN
${history}
USER'S HISTORY NEWS END
CANDIDATE NEWS BEGIN
${candidate}
CANDIDATE NEWS END
# Recommendation Process:
1. Extract Keywords from News Content: Begin by extracting keywords that accurately describe and represent each news item. These keywords should capture the essence of the news content.
2. Analyze User's History News:
2.1 Extract a collection of keywords from all 'User's History News'.
2.2 Group these keywords into clusters representing related concepts or meanings, known as 'topic'. A topic typically consists of frequently co-occurring words reflecting underlying topics or discussions. For example, a cluster including words like 'NBA', 'player', and 'match' closely relates to the concept of 'sports'. If a user's historical browsing news frequently involves these words, it can be inferred that they are interested in 'sports'.
2.3 The aim here is to analyze the keyword collection to summarize and infer topics that the user is interested in.
3. Match Candidate News with User's Interests:
3.1 Extract keywords from each 'Candidate News'.
3.2 Analyze how well the keywords extracted from each Candidate News match the user's topics of interest and DON'T let the sequence order of the 'CANDIDATE NEWS' influence the ranking.
3.3 The degree of match is defined by how closely the keywords in a candidate news item relate to the corresponding topic. For example, if a user is interested in 'sports' and a candidate news item mentions words like 'NBA' and 'player', it can be considered a perfect match for the user's interest, potentially scoring 10 out of 10 on an assessment scale. Conversely, if a candidate news item focuses on topics like 'dog' and 'cat' related to 'pets', it would not match the user's interest in 'sports' and would rank lower in the recommendation list.
# Output Format:
- The first part of the output should summarize the user's most focused topics, starting with "Here are the user's interested topics and their related keyword collections: #topic: #keyword,#keyword,etc;...". '#topic' should be a specific concept. '#keyword' should be replaced with the corresponding keywords from the 'USER'S HISTORY NEWS' set and should relate to the specific '#topic'. 
- The second part should include up to 10 most relevant news from the CANDIDATE NEWS set in the format "#news: The extracted keywords of this news is: #keyword,#keyword,etc. The matched topics are: #topic,#topic,etc.". Replace '#news' with the corresponding news headline; '#keyword' and '#keyword' are corresponding keywords extracted from the headline, and '#topic' are specific topics extracted from 'USER'S HISTORY NEWS' as mentioned in the first part. If no topic is found, output 'There is no matched topic.'.
- At last, the output needs to rank these relevant news by their relevance to the user's summarized interest in the format: "The top 10 recommended news headlines, ranked solely by relevance to the user's interests, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
# Here is the output:
Think step by step and give your answer.
"""

template8 = """News recommendation involves two main types of data: 'USER'S HISTORY NEWS', which includes news headlines previously clicked by a user, sorted by the time of click, with earlier clicks appearing first, and 'CANDIDATE NEWS', which are the potential news headlines waiting to be recommended. The recommendation process entails summarizing users' preferences and interests based on their historical clicks, then filtering and ranking candidate news according to how well they match these preferences and interests, with higher relevance leading to higher ranking. The format of 'USER'S HISTORY NEWS' is in 'H#: #news', where 'H#' is the ID of the news and '#news' contains the news headline. The format of 'CANDIDATE NEWS' is in 'C#: #news', where 'C#' is the ID of the news and '#news' contains the news headline.
# INPUT
USER'S HISTORY NEWS BEGIN
${history}
USER'S HISTORY NEWS END
CANDIDATE NEWS BEGIN
${candidate}
CANDIDATE NEWS END
# Recommendation Process:
1. Extract Keywords from News Content: Begin by extracting keywords that accurately describe and represent each news item. These keywords should capture the essence of the news content.
2. Analyze User's History News:
2.1 Extract a collection of keywords from all 'User's History News'.
2.2 Group these keywords into clusters representing related concepts or meanings, known as 'topic'. A topic typically consists of frequently co-occurring words reflecting underlying topics or discussions. For example, a cluster including words like 'NBA', 'player', and 'match' closely relates to the concept of 'sports'. If a user's historical browsing news frequently involves these words, it can be inferred that they are interested in 'sports'.
2.3 The aim here is to analyze the keyword collection to summarize and infer topics that the user is interested in.
3. Match Candidate News with User's Interests:
3.1 Extract keywords from each 'Candidate News'.
3.2 Analyze how well the keywords extracted from each Candidate News match the user's topics of interest and DON'T let the sequence order of the 'CANDIDATE NEWS' influence the ranking.
3.3 The degree of match is defined by how closely the keywords in a candidate news item relate to the corresponding topic. For example, if a user is interested in 'sports' and a candidate news item mentions words like 'NBA' and 'player', it can be considered a perfect match for the user's interest, potentially scoring 10 out of 10 on an assessment scale. Conversely, if a candidate news item focuses on topics like 'dog' and 'cat' related to 'pets', it would not match the user's interest in 'sports' and would rank lower in the recommendation list.
# Output Format:
- The first part of the output should summarize the user's most focused topics, starting with "Here are the user's interested topics and their related keyword collections: #topic: #keyword,#keyword,etc;...". '#topic' should be a specific concept. '#keyword' should be replaced with the corresponding keywords from the 'USER'S HISTORY NEWS' set and should relate to the specific '#topic'. 
- The second part should include up to 10 most relevant news from the CANDIDATE NEWS set in the format "#news: The extracted keywords of this news is: #keyword,#keyword,etc. The matched topics are: #topic,#topic,etc.". Replace '#news' with the corresponding news headline; '#keyword' and '#keyword' are corresponding keywords extracted from the headline, and '#topic' are specific topics extracted from 'USER'S HISTORY NEWS' as mentioned in the first part. If no topic is found, output 'There is no matched topic.'.
- At last, the output needs to rank these relevant news by their relevance to the user's summarized interest in the format: "The top 10 recommended news headlines, ranked solely by relevance to the user's interests, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
# Here is the output:
"""

template9 = """News recommendation involves two main data types: 'USER'S HISTORY NEWS', which includes news headlines previously clicked by a user, sorted by the time of click, with earlier clicks appearing first, and 'CANDIDATE NEWS'. The recommendation process entails summarizing users' preferences and interests based on their historical clicks, then filtering and ranking candidate news according to how well they match these preferences and interests, with higher relevance leading to higher ranking. The format of 'USER'S HISTORY NEWS' is in 'H#: #news', where 'H#' is the ID of the news and '#news' contains the news headline. The format of 'CANDIDATE NEWS' is in 'C#: #news', where 'C#' is the ID of the news and '#news' contains the news headline. 
# INPUT
USER'S HISTORY NEWS BEGIN
${history}
USER'S HISTORY NEWS END
CANDIDATE NEWS BEGIN
${candidate}
CANDIDATE NEWS END
# Recommendation Process:
1. Analyze User's History News:
1.1 Extract a collection of keywords from all 'User's History News'. These keywords can accurately describe and represent the specific news item.
1.2 Group these keywords into clusters representing related concepts or meanings, known as 'topic'. A topic typically consists of frequently co-occurring words reflecting underlying topics or discussions. For example, a cluster including words like 'NBA', 'player', and 'match' closely relates to the concept of 'sports'. If a user's historical browsing news frequently involves these words, it implies that they are interested in 'sports'.
1.3 Analyze the keyword collection to summarize and infer topics that the user is interested in.
2. Match Candidate News with User's Interests:
2.1 Extract keywords from each 'Candidate News'. These keywords can accurately describe and represent the specific news item.
2.2 Analyze how well the keywords extracted from each Candidate News match the user's topics of interest and recommend news based on this alignment INSTEAD OF  the 'CANDIDATE NEWS' sequence order.
2.3 This alignment is defined by how closely the keywords in a candidate news item relate to the corresponding topic. For example, if a user is interested in 'sports' and a candidate news item mentions words like 'NBA' and 'player', it can be considered a perfect match for the user's interest. Conversely, if a candidate news item focuses on topics like 'dog' and 'cat' related to 'pets', it would not match the user's interest in 'sports' and would rank lower in the recommendation list.
# Here is the output:"""

template10 = """News recommendation involves two main data types: 'USER'S HISTORY NEWS', which includes news headlines previously clicked by a user, sorted by the time of click, with earlier clicks appearing first, and 'CANDIDATE NEWS'. The recommendation process entails summarizing users' preferences and interests based on their historical clicks, then filtering and ranking candidate news according to how well they match these preferences and interests, with higher relevance leading to higher ranking. The format of 'USER'S HISTORY NEWS' is in 'H#: #news', where 'H#' is the ID of the news and '#news' contains the news headline. The format of 'CANDIDATE NEWS' is in 'C#: #news', where 'C#' is the ID of the news and '#news' contains the news headline. 
# INPUT
USER'S HISTORY NEWS BEGIN
${history}
USER'S HISTORY NEWS END
CANDIDATE NEWS BEGIN
${candidate}
CANDIDATE NEWS END
# Recommendation Process:
1. Analyze User's History News:
1.1 Extract a collection of keywords from all 'User's History News'. These keywords can accurately describe and represent the specific news item.
1.2 Group these keywords into clusters representing related concepts or meanings, known as 'topic'. A topic typically consists of frequently co-occurring words reflecting underlying topics or discussions. For example, a cluster including words like 'NBA', 'player', and 'match' closely relates to the concept of 'sports'. If a user's historical browsing news frequently involves these words, it implies that they are interested in 'sports'.
1.3 Analyze the keyword collection to summarize and infer topics that the user is interested in.
2. Match Candidate News with User's Interests:
2.1 Extract keywords from each 'Candidate News'. These keywords can accurately describe and represent the specific news item.
2.2 Analyze how well the keywords extracted from each Candidate News match the user's topics of interest and recommend news based on this alignment INSTEAD OF  the 'CANDIDATE NEWS' sequence order.
2.3 This alignment is defined by how closely the keywords in a candidate news item relate to the corresponding topic. For example, if a user is interested in 'sports' and a candidate news item mentions words like 'NBA' and 'player', it can be considered a perfect match for the user's interest. Conversely, if a candidate news item focuses on topics like 'dog' and 'cat' related to 'pets', it would not match the user's interest in 'sports' and would rank lower in the recommendation list.
# Here is the output:
Think Step by Step and Output the recommendation in a list."""

template11 = """News recommendation involves two main data types: 'USER'S HISTORY NEWS', which includes news headlines previously clicked by a user, sorted by the time of click, with earlier clicks appearing first, and 'CANDIDATE NEWS'. The recommendation process entails summarizing users' preferences and interests based on their historical clicks, then filtering and ranking candidate news according to how well they match these preferences and interests, with higher relevance leading to higher ranking. The format of 'USER'S HISTORY NEWS' is in 'H#: #news', where 'H#' is the ID of the news and '#news' contains the news headline. The format of 'CANDIDATE NEWS' is in 'C#: #news', where 'C#' is the ID of the news and '#news' contains the news headline. 
# INPUT
USER'S HISTORY NEWS BEGIN
${history}
USER'S HISTORY NEWS END
CANDIDATE NEWS BEGIN
${candidate}
CANDIDATE NEWS END
# Recommendation Process:
1. Analyze User's History News:
1.1 Extract a collection of keywords from all 'User's History News'. These keywords can accurately describe and represent the specific news item.
1.2 Group these keywords into clusters representing related concepts or meanings, known as 'topic'. A topic typically consists of frequently co-occurring words reflecting underlying topics or discussions. For example, a cluster including words like 'NBA', 'player', and 'match' closely relates to the concept of 'sports'. If a user's historical browsing news frequently involves these words, it implies that they are interested in 'sports'.
1.3 Analyze the keyword collection to summarize and infer topics that the user is interested in.
2. Match Candidate News with User's Interests:
2.1 Extract keywords from each 'Candidate News'. These keywords can accurately describe and represent the specific news item.
2.2 Analyze how well the keywords extracted from each Candidate News match the user's topics of interest and recommend news based on this alignment INSTEAD OF the 'CANDIDATE NEWS' sequence order.
2.3 This alignment is defined by how closely the keywords in a candidate news item relate to the corresponding topic. For example, if a user is interested in 'sports' and a candidate news item mentions words like 'NBA' and 'player', it can be considered a perfect match for the user's interest. Conversely, if a candidate news item focuses on topics like 'dog' and 'cat' related to 'pets', it would not match the user's interest in 'sports' and would rank lower in the recommendation list.
# Here is the output:
Output the recommendation list based on the matching topic between the 'CANDIDATE NEWS' and 'User's History News'. DON'T be influenced by the 'CANDIDATE NEWS' sequence order. DON'T give the news a higher rank because the news appears in the front of the 'CANDIDATE NEWS' set.
"""
template12 = """News recommendation involves two main data types: 'USER'S HISTORY NEWS', which includes news headlines previously clicked by a user, sorted by the time of click, with earlier clicks appearing first, and 'CANDIDATE NEWS'. The recommendation process entails summarizing users' preferences and interests based on their historical clicks, then filtering and ranking candidate news according to how well they match these preferences and interests, with higher relevance leading to higher ranking. The format of 'USER'S HISTORY NEWS' is in 'H#: #news', where 'H#' is the ID of the news and '#news' contains the news headline. The format of 'CANDIDATE NEWS' is in 'C#: #news', where 'C#' is the ID of the news and '#news' contains the news headline. 
# INPUT
USER'S HISTORY NEWS BEGIN
${history}
USER'S HISTORY NEWS END
CANDIDATE NEWS BEGIN
${candidate}
CANDIDATE NEWS END
# Recommendation Process:
1. Analyze User's History News:
1.1 Extract a collection of keywords from all 'User's History News'. These keywords can accurately describe and represent the specific news item.
1.2 Group these keywords into clusters representing related concepts or meanings, known as 'topic'. A topic typically consists of frequently co-occurring words reflecting underlying topics or discussions. For example, a cluster including words like 'NBA', 'player', and 'match' closely relates to the concept of 'sports'. If a user's historical browsing news frequently involves these words, it implies that they are interested in 'sports'.
1.3 Analyze the keyword collection to summarize and infer topics that the user is interested in.
2. Match Candidate News with User's Interests:
2.1 Extract keywords from each 'Candidate News'. These keywords can accurately describe and represent the specific news item.
2.2 Analyze how well the keywords extracted from each Candidate News match the user's topics of interest and recommend news based on this alignment INSTEAD OF the 'CANDIDATE NEWS' sequence order.
2.3 This alignment is defined by how closely the keywords in a candidate news item relate to the corresponding topic. For example, if a user is interested in 'sports' and a candidate news item mentions words like 'NBA' and 'player', it can be considered a perfect match for the user's interest. Conversely, if a candidate news item focuses on topics like 'dog' and 'cat' related to 'pets', it would not match the user's interest in 'sports' and would rank lower in the recommendation list.
# Output Format:
- The first part of the output should summarize the user's most focused topics, starting with "Here are the user's interested topics and their related keyword collections: #topic: #keyword,#keyword,etc;...". '#topic' should be a specific concept. '#keyword' should be replaced with the corresponding keywords from the 'USER'S HISTORY NEWS' set and should relate to the specific '#topic'. 
- The second part should include up to 10 most relevant news from the CANDIDATE NEWS set in the format "#news: The extracted keywords of this news is: #keyword,#keyword,etc. The matched topics are: #topic,#topic,etc.". Replace '#news' with the corresponding news headline; '#keyword' and '#keyword' are corresponding keywords extracted from the headline, and '#topic' are specific topics extracted from 'USER'S HISTORY NEWS' as mentioned in the first part. If no topic is found, output 'There is no matched topic.'.
- At last, the output needs to rank these relevant news by their relevance to the user's summarized interest in the format: "The top 10 recommended news headlines, ranked solely by relevance to the user's interests, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
# Here is the output:
Output the recommendation list based on the matching topic between the 'CANDIDATE NEWS' and 'User's History News'. DON'T be influenced by the 'CANDIDATE NEWS' sequence order. DON'T give the news a higher rank because the news appears in the front of the 'CANDIDATE NEWS' set.
"""
template14 = """News recommendation involves two main data types: 'USER'S HISTORY NEWS', which includes news headlines previously clicked by a user, sorted by the time of click, with earlier clicks appearing first, and 'CANDIDATE NEWS'. The recommendation process entails summarizing users' preferences and interests based on their historical clicks, then filtering and ranking candidate news according to how well they match these preferences and interests, with higher relevance leading to higher ranking. The format of 'USER'S HISTORY NEWS' is in 'H#: #news', where 'H#' is the ID of the news and '#news' contains the news headline. The format of 'CANDIDATE NEWS' is in 'C#: #news', where 'C#' is the ID of the news and '#news' contains the news headline. 
# INPUT
USER'S HISTORY NEWS BEGIN
${history}
USER'S HISTORY NEWS END
CANDIDATE NEWS BEGIN
${candidate}
CANDIDATE NEWS END
# Recommendation Process:
1. Analyze User's History News:
1.1 Extract a collection of keywords from all 'User's History News'. These keywords can accurately describe and represent the specific news item.
1.2 Group these keywords into clusters representing related concepts or meanings, known as 'topic'. A topic typically consists of frequently co-occurring words reflecting underlying topics or discussions. For example, a cluster including words like 'NBA', 'player', and 'match' closely relates to the concept of 'sports'. If a user's historical browsing news frequently involves these words, it implies that they are interested in 'sports'.
1.3 Analyze the keyword collection to summarize and infer topics that the user is interested in.
2. Match Candidate News with User's Interests:
2.1 Extract keywords from each 'Candidate News'. These keywords can accurately describe and represent the specific news item.
2.2 Analyze how well the keywords extracted from each Candidate News match the user's topics of interest and recommend news based on this alignment INSTEAD OF the 'CANDIDATE NEWS' sequence order.
2.3 This alignment is defined by how closely the keywords in a candidate news item relate to the corresponding topic. For example, if a user is interested in 'sports' and a candidate news item mentions words like 'NBA' and 'player', it can be considered a perfect match for the user's interest. Conversely, if a candidate news item focuses on topics like 'dog' and 'cat' related to 'pets', it would not match the user's interest in 'sports' and would rank lower in the recommendation list.
# Output Format:
- The first part of the output should summarize the user's most focused topics, starting with "Here are the user's interested topics and their related keyword collections: #topic: #keyword,#keyword,etc;...". '#topic' should be a specific concept. '#keyword' should be replaced with the corresponding keywords from the 'USER'S HISTORY NEWS' set and should relate to the specific '#topic'. 
- The second part should start with "Next, the alignment of candidate news and user's interested topics are: #news: The extracted keywords of this news is: #keyword,#keyword,etc. The matched topics are: #topic,#topic,etc.". Replace '#news' with the corresponding news headline; '#keyword' and '#keyword' are corresponding keywords extracted from the headline, and '#topic' are specific topics extracted from 'USER'S HISTORY NEWS' as mentioned in the first part. 
- Finally, rank candidate news according to their relevance to the user's interest in the format: "The top 10 recommended news headlines, ranked solely by relevance to the user's interests, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
# Here is the output:
Output the recommendation list based on the matching topic between the 'CANDIDATE NEWS' and 'User's History News'. DON'T be influenced by the 'CANDIDATE NEWS' sequence order. DON'T give the news a higher rank because the news appears in the front of the 'CANDIDATE NEWS' set."""

template15 = """News recommendation involves two main data types: 'USER'S HISTORY NEWS', which includes news headlines previously clicked by a user, sorted by the time of click, with earlier clicks appearing first, and 'CANDIDATE NEWS'. The recommendation process entails summarizing users' preferences and interests based on their historical clicks, then filtering and ranking candidate news according to how well they match these preferences and interests, with higher relevance leading to higher ranking. The format of 'USER'S HISTORY NEWS' is in 'H#: #news', where 'H#' is the ID of the news and '#news' contains the news headline. The format of 'CANDIDATE NEWS' is in 'C#: #news', where 'C#' is the ID of the news and '#news' contains the news headline. 
# INPUT
USER'S HISTORY NEWS BEGIN
${history}
USER'S HISTORY NEWS END
CANDIDATE NEWS BEGIN
${candidate}
CANDIDATE NEWS END
# Recommendation Process:
1. Analyze User's History News:
1.1 Extract a collection of keywords from all 'User's History News'. These keywords can accurately describe and represent the specific news item.
1.2 Group these keywords into clusters representing related concepts or meanings, known as 'topic'. A topic typically consists of frequently co-occurring words reflecting underlying topics or discussions. For example, a cluster including words like 'NBA', 'player', and 'match' closely relates to the concept of 'sports'. If a user's historical browsing news frequently involves these words, it implies that they are interested in 'sports'.
1.3 Analyze the keyword collection to summarize and infer topics that the user is interested in.
2. Match Candidate News with User's Interests:
2.1 Extract keywords from each 'Candidate News'. These keywords can accurately describe and represent the specific news item.
2.2 Analyze how well the keywords extracted from each Candidate News match the user's topics of interest and recommend news based on this alignment INSTEAD OF the 'CANDIDATE NEWS' sequence order.
2.3 This alignment is defined by how closely the keywords in a candidate news item relate to the corresponding topic. For example, if a user is interested in 'sports' and a candidate news item mentions words like 'NBA' and 'player', it can be considered a perfect match for the user's interest. Conversely, if a candidate news item focuses on topics like 'dog' and 'cat' related to 'pets', it would not match the user's interest in 'sports' and would rank lower in the recommendation list.
# Output Format:
Rank candidate news according to their relevance to the user's interest in the format: "The top 10 recommended news headlines, ranked solely by relevance to the user's interests, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
# Here is the output:
Output the recommendation list based on the matching topic between the 'CANDIDATE NEWS' and 'User's History News'. DON'T be influenced by the 'CANDIDATE NEWS' sequence order. DON'T give the news a higher rank because the news appears in the front of the 'CANDIDATE NEWS' set."""

template16 = """News recommendation involves two main data types: 'USER'S HISTORY NEWS', which includes news headlines previously clicked by a user, sorted by the time of click, with earlier clicks appearing first, and 'CANDIDATE NEWS'. The recommendation process entails summarizing users' preferences and interests based on their historical clicks, then filtering and ranking candidate news according to how well they match these preferences and interests, with higher relevance leading to higher ranking. The format of 'USER'S HISTORY NEWS' is in 'H#: #news', where 'H#' is the ID of the news and '#news' contains the news headline. The format of 'CANDIDATE NEWS' is in 'C#: #news', where 'C#' is the ID of the news and '#news' contains the news headline. 
# INPUT
USER'S HISTORY NEWS BEGIN
${history}
USER'S HISTORY NEWS END
CANDIDATE NEWS BEGIN
${candidate}
CANDIDATE NEWS END
# Recommendation Process:
1. Analyze User's History News:
1.1 Extract a collection of keywords from all 'User's History News'. These keywords can accurately describe and represent the specific news item.
1.2 Group these keywords into clusters representing related concepts or meanings, known as 'topic'. A topic typically consists of frequently co-occurring words reflecting underlying topics or discussions. For example, a cluster including words like 'NBA', 'player', and 'match' closely relates to the concept of 'sports'. If a user's historical browsing news frequently involves these words, it implies that they are interested in 'sports'.
1.3 Analyze the keyword collection to summarize and infer topics that the user is interested in.
2. Match Candidate News with User's Interests:
2.1 Extract keywords from each 'Candidate News'. These keywords can accurately describe and represent the specific news item.
2.2 Analyze how well the keywords extracted from each Candidate News match the user's topics of interest and recommend news based on this alignment INSTEAD OF the 'CANDIDATE NEWS' sequence order.
2.3 This alignment is defined by how closely the keywords in a candidate news item relate to the corresponding topic. For example, if a user is interested in 'sports' and a candidate news item mentions words like 'NBA' and 'player', it can be considered a perfect match for the user's interest. Conversely, if a candidate news item focuses on topics like 'dog' and 'cat' related to 'pets', it would not match the user's interest in 'sports' and would rank lower in the recommendation list.
# Output Format:
Summarize the user's interest and rank candidate news according to their relevance to the user's interest in the format: "The top 10 recommended news headlines, ranked solely by relevance to the user's interests: <START>C#, C#, C#, C#, C#, C#, C#, C#, C#, C#<END>". Explain the ranking results.
# Here is the output:
Output the recommendation list based on the matching topic between the 'CANDIDATE NEWS' and 'User's History News'. DON'T be influenced by the 'CANDIDATE NEWS' sequence order. DON'T give the news a higher rank because the news appears in the front of the 'CANDIDATE NEWS' set."""
