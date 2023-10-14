import pandas as pd
import numpy as np
import openai
import time
import os
from metrics import calculate_metrics

df = pd.read_csv("./sampled_100.csv")

openai.api_key = os.getenv("OPENAI_API_KEY")

def build_user_input(history, candidate):
    
    user_inputs = [
    f"""1. Understanding Historical News Titles:
    Examine each historical news title from the user's history.
    Based on your knowledge and understanding, rewrite each title to be more informative while ensuring the content remains consistent. You may augment the titles with additional relevant knowledge where appropriate. \n History: {history}""", 

    """2. User Profiling:
    Utilizing the rewritten historical news titles, create a user profile that reflects their interests and preferences. Elaborate on the user’s persona through a short narrative that encapsulates their likely interests, drawing from the themes observed in the historical titles.""",

    f"""3. Rewriting Candidate News Titles:
    Similar to the process with historical news titles, rewrite the candidate news titles to be more informative. \n
    Candidate : {candidate}""",

    """4. Categorizing Candidate News:
    Based on the user’s profile and historical news titles, estimate the likelihood of the user clicking on each rewritten candidate news title.
    Categorize the rewritten candidate news titles into three groups based on the estimated likelihood of a click: Highly Likely, Moderately Likely, and Unlikely. Provide rationale for the categorization.""",

    """5. Sorting Within Categories:
    Within each of the three categories, sort the candidate news titles in descending order of likelihood of being clicked. Provide rationale for the order."""


    """6. Returning Sorted List:
    Merge the sorted lists of candidate news IDs from the 'Highly Likely', 'Moderately Likely', and 'Unlikely' categories into a single list. Format the final compiled list as "C1, C2, C3, C4, etc.", where each 'C' represents the ID of a candidate news title. Only return final compiled list with all candidate news ID"""

    ]

    return user_inputs


instruction = (
'''You are the Perfect News Recommender, an advanced AI developed to help users discover news stories they will find intriguing and informative based on their past reading history. Your mission is to curate a personalized news feed for each user, ensuring they stay informed and engaged with the world around them.
''')


def continue_conversation(user_inputs):
    messages = [{"role": "system", "content": instruction}]

    for single_input in user_inputs:
        messages.append({"role": "user", "content": single_input})
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        frequency_penalty=0,
        presence_penalty=0
        )
        messages.append({
            "role": "assistant",
            "content": response['choices'][0]['message']['content']
        })

    return messages


results = []
for index, row in df.iterrows():
    user_input = build_user_input(row['history'], row['candidate'])
    total_conversation = continue_conversation(user_input)
    sorted_candidates = total_conversation[-1]['content'].replace(" ", "").split(',')  

    print("index: ", index, " ", "list: ", sorted_candidates)

    time.sleep(10)
    true_label = row['label'].split(',')
    auc, mrr, ndcg5, ndcg10 = calculate_metrics(true_label, sorted_candidates)
    results.append((row['impression_id'], ",".join(sorted_candidates), auc, mrr, ndcg5, ndcg10))

    
results_df = pd.DataFrame(results, columns=['impression_id', 'sorted_candidates', 'AUC', 'MRR', 'nDCG@5', 'nDCG@10'])

results_df.to_csv('sorted_results_cot_zero.csv', index=False)

mean_auc = results_df['AUC'].mean()
mean_mrr = results_df['MRR'].mean()
mean_ndcg_at_5 = results_df['nDCG@5'].mean()
mean_ndcg_at_10 = results_df['nDCG@10'].mean()

print(f"Overall AUC: {mean_auc:.4f}")
print(f"Overall MRR: {mean_mrr:.4f}")
print(f"Overall nDCG@5: {mean_ndcg_at_5:.4f}")
print(f"Overall nDCG@10: {mean_ndcg_at_10:.4f}")