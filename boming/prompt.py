def build_prompt_template0(history, candidate):
    user_inputs = f"""
    # Input
    User's History News:
    {history}
    Candidate News:
    {candidate}

    # Recommendation Process:
    1. 'User's History News' contains headlines that have engaged the user, revealing their interests through one broad key theme and five specific keywords.
    2. 'Candidate News' consists of new headlines. The order of these headlines is not relevant to their ranking.
    3. Your objective is to select the top 10 headlines from 'Candidate News' that are most closely aligned with the user's broad theme and specific keywords as indicated in 'User's History News'.

    # Recommendation Process:
    1. Analyze 'User's History News' to identify one broad key theme and extract five specific keywords reflecting the user's interests.
    2. For 'Candidate News', identify the main theme and extract five keywords from each headline, disregarding their initial sequence, to evaluate their relevance to the user’s interests.
    3. Rank the 'Candidate News' headlines by relevance to the broad theme and specific keywords identified in the user's history, not by their original order.

    # Output Format:
    - Begin with: "The top 10 recommended news headlines, ranked by relevance to the user's broad theme and specific keywords, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
    - Include a justification for each headline's ranking, emphasizing their alignment with the broad theme and specific keywords: "C# relates to broad theme X and includes keywords A, B, C, closely matching the user's interest as shown in headlines H#, H#, H#."
    - Follow this structure for each of the top 10 headlines.
    - Limit the total output to 200 words, focusing on the alignment of the broad theme and specific keywords rather than the original sequence of 'Candidate News'."
    """

    return user_inputs

def build_prompt_template1(history, candidate):
    user_inputs = f"""
    # Input:
    User's History News:
    {history}
    Candidate News:
    {candidate}

    # Task Description:
    1. 'User's History News' features headlines that have previously engaged the user, signaling their interests through key themes and specific keywords.
    2. 'Candidate News' presents a set of headlines not yet seen by the user. The sequence of these headlines should not influence the ranking.
    3. Your objective is to select the top 10 headlines from 'Candidate News' that most closely resonate with the user's interests as reflected in both key themes and specific keywords from 'User's History News'.

    # Recommendation Process:
    1. Analyze each historical news piece to identify 1 key theme and extract 5 specific keywords, capturing both broad and detailed aspects of the user's interests.
    2. For each piece of candidate news, identify 1 key theme and 5 specific keywords, emphasizing their potential relevance to the historical themes and keywords, disregarding their initial order.
    3. Rank the 'Candidate News' headlines by relevance based on the alignment with the key themes and keywords from the user's history, not by their original placement in the list.

    # Output Format:
    - Start with the phrase: "The top 10 recommended news headlines, ranked by relevance to both historical themes and keywords, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
    - Provide a relevance-based justification for each headline's ranking, such as: "C# pertains to key theme X and includes keywords A, B, C, aligning with the user's interest shown in headlines H#, H#, H#."
    - Maintain this structure for each of the top 10 headlines.
    - The total output should not exceed a 200-word limit, focusing on the alignment of key themes and specific keywords rather than the original order of 'Candidate News'.
    """

    return user_inputs

def build_prompt_template2(history, candidate):
    
    user_inputs = f"""
    # Input:
    User's History News:
    {history}
    Candidate News:
    {candidate}

    # Task Description:
    1. 'User's History News' features headlines that have previously engaged the user, signaling their interests through specific keywords.
    2. 'Candidate News' presents a set of headlines not yet seen by the user. The sequence of these headlines should not influence the ranking.
    3. Your objective is to select the top 10 headlines from 'Candidate News' that most closely resonate with the user's interests as reflected in both key themes and specific keywords from 'User's History News'.

    # Recommendation Process:
    1. Analyze each historical news piece to extract 5 specific keywords, capturing the detailed aspects of the user's interests.
    2. For each piece of candidate news, identify 5 specific keywords, emphasizing their potential relevance to the historical themes and keywords, disregarding their initial order.
    3. Rank the 'Candidate News' headlines by relevance based on the alignment with the keywords from the user's history, not by their original placement in the list.

    # Output Format:
    - Start with the phrase: "The top 10 recommended news headlines, ranked by relevance to both historical and keywords, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
    - Provide a relevance-based justification for each headline's ranking, such as: "C# includes keywords A, B, C, aligning with the user's interest shown in headlines H#, H#, H#."
    - Maintain this structure for each of the top 10 headlines.
    - The total output should not exceed a 200-word limit, focusing on the alignment of specific keywords rather than the original order of 'Candidate News'.
    """

    return user_inputs

def build_instruction():
    instruction = '''You serve as a personalized news recommendation system'''

    return instruction

def build_prompt_template99(history, candidate):

    user_inputs = f"""
    1. Understanding Historical News Titles:
    Examine each historical news title from the user's history.
    Based on your knowledge and understanding, rewrite each title to be more informative while ensuring the content remains consistent. You may augment the titles with additional relevant knowledge where appropriate. \n History: 
    {history}, 

    2. User Profiling:
    Utilizing the rewritten historical news titles, create a user profile that reflects their interests and preferences. Elaborate on the user’s persona through a short narrative that encapsulates their likely interests, drawing from the themes observed in the historical titles.

    3. Rewriting Candidate News Titles:
    Similar to the process with historical news titles, rewrite the candidate news titles to be more informative.
    Candidate : 
    {candidate},

    4. Categorizing Candidate News:
    Based on the user's profile and historical news titles, estimate the likelihood of the user clicking on each rewritten candidate news title.
    Categorize the rewritten candidate news titles into three groups based on the estimated likelihood of a click: Highly Likely, Moderately Likely, and Unlikely. Provide rationale for the categorization.

    5. Sorting Within Categories:
    Within each of the three categories, sort the candidate news titles in descending order of likelihood of being clicked. Provide rationale for the order.

    6. Returning Sorted List:
    Merge the sorted lists of candidate news IDs from the 'Highly Likely', 'Moderately Likely', and 'Unlikely' categories into a single list. Format the final compiled list as "C1, C2, C3, C4, etc.", where each 'C' represents the ID of a candidate news title. Only return final compiled list with all candidate news ID
    """

    return user_inputs

def build_prompt_template10(history, candidate):
    user_inputs = f"""

    User's History News:
    {history}
    Candidate News:
    {candidate}
    
    # Process Overview
    - Extract specific, significant keywords from the each historical news, indicative of their detailed interests.
    - Identify precise keywords for each candidate news item, focusing on unique and prominent aspects.

    # Ranking Principle
    - The ranking is primarily based on the match and quantity of keywords between the candidate news and the user's historical interests.
    - News items with a higher number of keywords matching or closely related to the user's interests are ranked higher.
    - Secondary consideration is given to the presence of keywords that are relevant but not directly matching, indicating a broader relevance.

    
    # Output Format: Ranked Specific Keywords
    - Present the top 10 recommended news headlines, ranked solely by their relevance to the user's interests.
    - Output: "Top 10 recommended news headlines, ranked by relevance, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
    """
    
    return user_inputs

def build_prompt_template15(history, candidate):
    user_inputs = f"""

    User's History News:
    {history}
    Candidate News:
    {candidate}
    
    # Recommendation Process:
    1. Analyze each user's historical news to extract 5 specific keywords.
    2. For each piece of candidate news, identify 5 specific keywords, emphasizing their potential relevance to the historical keywords.
    3. Match each candidate news with the total historical news keywords. Prioritize those with overlapping or closely related themes, indicating a higher relevance to the user's interests.

    # Output Format:
    - Start with the phrase: "The top 10 recommended candidate news, ranked solely by relevance to the total historical keywords, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
    - The total output should not exceed a 200-word limit, focusing on the alignment of keywords rather than the original order of 'Candidate News'.
    """
    
    return user_inputs

def build_improved_prompt50(history, candidate):
    user_inputs = f"""
    # Input
    User's History News:
    {history}
    Candidate News:
    {candidate}

    # Task Description:
    1. 'User's History News' features headlines that have previously engaged the user, signaling their interests.
    2. 'Candidate News' presents a set of headlines not yet seen by the user. The sequence of these headlines should not influence the ranking.
    3. Your objective is to impartially select the top 10 headlines from 'Candidate News' that most closely resonate with the user's interests as reflected in 'User's History News'.

    # Recommendation Process:
    1. Analyze each historical news piece to extract 1 key themes and 5 specific keywords, capturing both broad and detailed aspects.
    2. For each piece of candidate news, identify 1 key themes and 5 specific keywords, disregarding their initial order, emphasizing their potential relevance to the historical themes and keywords.
    3. Strategically rank the 'Candidate News' headlines by relevance, not by their original placement in the list.

    # Output Format:
    - Start with the phrase: "The top 10 recommended CANDIDATE NEWS items, ranked by relevance to both historical themes and keywords, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
    - Proceed with a relevance-based justification for each headline's ranking, such as: "C# pertains to key theme X, which align with the keywords O,P,Q shown in headlines H#, H#, H#."
    - Maintain this structure for each of the top 10 headlines.
    - The total output should not exceed a 200-word limit, focusing on the alignment of key themes and keywords rather than the original order of 'Candidate News'."""

    return user_inputs

def build_prompt_template51(history, candidate):
    user_inputs = f"""
    # Input
    User's History News:
    {history}
    Candidate News:
    {candidate}

    # Recommendation Process:
    1. Analyze each historical news piece to extract 5 key themes and 5 specific keywords, capturing both broad and detailed aspects.
    2. For each piece of candidate news, identify 5 key themes and 5 specific keywords, emphasizing their potential relevance to the historical themes and keywords.
    3. Match each candidate news with historical themes and keywords, prioritizing those with the highest overlap and relevance.

    # Output Format:
    - Do not explain reasons in the response and only return a python list of the first letter for each article.
    """
    return user_inputs

def build_prompt_template4(history, candidate):
    template4 = f"""
    # Input:
    User's History News:
    {history}
    Candidate News:
    {candidate}

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

    return template4

def build_prompt_template_base(history, candidate):
    
    template = f"""

    Generate a ranked list of news headlines based on user's reading preferences.

    User's History of Read Headlines:
    {history}

    List of Candidate News Headlines for Recommendation:
    {candidate}

    Task: Based on the user's history of read headlines, rank the candidate news headlines in order of their likelihood to interest the user. The ranking should predict which headlines the user is most likely to click on next.

    Expected Output Format:
    Ranked List: [Most likely to be clicked headline, Second most likely, ...]
    """

    return template

def build_prompt_template_detail(history, candidate):
    user_inputs = f"""
    # Input:
    User's History News:
    {history}
    Candidate News:
    {candidate}

    # Task Description:
    1. 'User's History News' consists of headlines the user has engaged with, indicating their interest areas. This section is vital for recognizing common themes and specific keywords defining the user's reading preferences.
    2. 'Candidate News' presents new headlines not yet seen by the user. The order of these headlines is random and should not influence the ranking.

    # Understanding Themes and Keywords:
    - A 'theme' is the overarching subject or topic of a news headline, such as 'technology', 'politics', or 'environment'.
    - 'Keywords' are specific, significant words or phrases within a headline that give insight into the more detailed aspects of the theme, like 'smartphones', 'elections', or 'climate change'.

    # Recommendation Process:
    1. From each headline in 'User's History News', identify one central theme and extract five key keywords. This identification captures both the general and specific interests of the user.
    2. For each headline in 'Candidate News', identify one primary theme and five relevant keywords, considering how they might relate to the historical themes and keywords.
    3. Rank the 'Candidate News' headlines based on their relevance. The ranking criteria should prioritize:
    - Headlines matching both the key themes and keywords from the user's history.
    - Next, prioritize headlines matching several keywords.
    - Then, headlines matching the theme.
    - Finally, include headlines that might be of interest based on the overall user profile.

    # Output Format:
    - Begin with: "The top 10 recommended news headlines, ranked by relevance to the user's historical themes and keywords, are: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10."
    - For each headline, provide a brief justification based on its theme and keyword alignment, e.g., "C1 aligns with the theme X and includes keywords A, B, C, matching the user's interest in headlines H1, H2, H3."
    - Follow this structure for all top 10 headlines.
    - Limit the total output to 200 words, focusing on the alignment of themes and keywords rather than the original order of 'Candidate News'.
    """

    return user_inputs