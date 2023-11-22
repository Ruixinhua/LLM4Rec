def build_prompt(history, candidate):
    user_inputs = f"""
    User's History News:
    {history}
    Candidate News:
    {candidate}

    # Recommendation Process:
    1. Analyze each user's historical news to extract 5 key themes, focusing on the most recurring topics or subjects.
    2. For each piece of candidate news, identify 5 central themes, emphasizing their potential relevance to the user’s historical interests.
    3. Match each candidate news with the user's historical news themes. Prioritize those with overlapping or closely related themes, indicating a higher relevance to the user's interests.

    # Output Format:
    - Start with the phrase: "The top 10 recommended news headlines, ranked solely by relevance to the user's interests, are: C#, C#, C#, C#, C#, C#, C#, C#, C#, C#."
    - Proceed with a relevance-based justification for each headline's ranking, such as: "C# pertains to topics X, Y, Z, which align with the user's interest shown in headlines H#, H#, H#."
    - Maintain this structure for each of the top 10 headlines.
    - The total output should not exceed a 200-word limit, focusing on the alignment of topics rather than the original order of 'Candidate News'.
    """

    return user_inputs


def build_prompt_temple1(history, candidate):
    user_inputs = f"""
    User's History News:
    {history}
    Candidate News:
    {candidate}

    #Task Description:
    1. The goal is to analyze and compare the content of 'User's History News' and 'Candidate News'.
    2. 'User's History News' consists of headlines that the user has previously engaged with.
    3. 'Candidate News' features a set of new headlines not yet seen by the user.
    4. The task is to find the similarities between the two sets of news to identify the most relevant 'Candidate News' headlines.
    
    # Analysis Process:
    1. Examine 'User's History News' to identify key topics, themes, and keywords.
    2. Evaluate 'Candidate News' for similar topics, themes, and keywords.
    3. Focus on the content and thematic overlap between the two news sets.
    
    # Output Format:
    1. Begin with: "The top 10 most relevant 'Candidate News' headlines, based on their similarity to 'User's History News', are: C#, C#, ..."
    2. Provide a brief explanation for each headline's inclusion, highlighting the specific similarities in topics or themes with 'User's History News'. For example: "C# is included because it shares similar themes X and Y with historical headlines H#, H#."
    3. Keep the total output concise, emphasizing the similarities rather than the individual content of the news headlines.
    """

    return user_inputs

def build_prompt_temple2(history, candidate):
    

    user_inputs = f"""
    User's History News:
    {history}
    Candidate News:
    {candidate}

    Identify and compare key elements from 'User's History News' and 'Candidate News'. Rank 'Candidate News' by the number of similar pairs with the whole 'User's History News', and return only the ranked list of candidate IDs.

    """

    return user_inputs

def build_instruction():
    instruction = '''You are a sophisticated text analysis and ranking system.'''

    return instruction

'''
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
Merge the sorted lists of candidate news IDs from the 'Highly Likely', 'Moderately Likely', and 'Unlikely' categories into a single list. Format the final compiled list as "C1, C2, C3, C4, etc.", where each 'C' represents the ID of a candidate news title. Only return final compiled list with all candidate news ID"""
'''


