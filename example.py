import itertools
import pickle
import yaml

from gensim import models, corpora
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import pandas
import praw


with open('creds.yaml', 'r') as f:
    creds = yaml.load(f)
print(creds)    
REDDIT_ID = creds['id']
REDDIT_SECRET = creds['secret']
APP_NAME = creds['app_name']

MY_SUBREDDIT = 'gradschool'
STOPWORDS = stopwords.words("english")
LEMMATIZER = WordNetLemmatizer()

reddit = praw.Reddit(client_id=REDDIT_ID, client_secret=REDDIT_SECRET, user_agent=APP_NAME)
subreddit = reddit.subreddit(MY_SUBREDDIT)

top_posts = subreddit.top(limit=1000)

subreddit_top_1000_posts_info = []
for submission in top_posts:
    d = {
        'title': submission.title,
        'id': submission.id,
        'body': submission.selftext,
        'created_ts': submission.created,
        'comments': submission.comments.list()
    }
    subreddit_top_1000_posts_info.append(d)

pickle.dump(subreddit_top_1000_posts_info, open('subreddit_top_1k_posts.pkl', 'wb'))

def get_body_wrapper(comment):
    try:
        print('success')
        return c.body
    except:
        print('more comments')
        return ''

def remove_stopwords(item):
    return [LEMMATIZER.lemmatize(i) for i in item if i not in STOPWORDS]

def do_lda(top_posts, n_topics):
    text = [d['body'] + ' '.join([get_body_wrapper(c) for c in d['comments']]) for d in top_posts]
    text = [t.lower().split(' ') for t in text]
    text = [remove_stopwords(t) for t in text]

    dictionary = corpora.Dictionary(text)
    dictionary.filter_extremes(no_below=0.05, no_above=0.5)
    corpus = [dictionary.doc2bow(text_item) for text_item in text]
    lda_model = models.LdaModel(corpus, num_topics=n_topics, alpha='auto', eval_every=5)
    for idx, topic in lda_model.show_topics(
        num_topics=n_topics, num_words=20, formatted=False
    ):
        print([(dictionary[int(w[0])], w[0]) for w in topic])
        print()
    topics_probas = lda_model[corpus]
    overall_probas = {i: 0 for i in range(n_topics)}
    for p in topics_probas:
        for proba in p:
            overall_probas[proba[0]] = overall_probas[proba[0]] + proba[1]

    denominator = sum(overall_probas.values())
    overall_probas = {k: v / denominator for k, v in overall_probas.items()}
    print(overall_probas)

do_lda(subreddit_top_1000_posts_info, 4)

