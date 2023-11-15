import pandas as pd

file_path = 'linkedin_posts.csv'
df = pd.read_csv(file_path)

def clean_post_content(content):
    start_phrase = "<p>Content : "
    end_phrase = "</p>"

    if content.startswith(start_phrase) and content.endswith(end_phrase):
        content = content[len(start_phrase):-len(end_phrase)]
    return content

df['cleaned_post'] = df['content'].apply(clean_post_content)

df['post_name'] = ['post' + str(i+1) for i in range(len(df))]

df = df.drop('content', axis=1)
df.to_csv('updated_data.csv', index=False)
