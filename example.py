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
import requests

# TODO: bursty events/events with positive or negative affect
# land of giants podcast (FAANG)
# legaladvice wrt big tech

# TODO: exploratory analysis
# TODO: dossier (frequent users, avg word count, character count, upvote distribution, sentiment, reading ease, stopword usage)
# avg word length, media usage, outlink domains, user age (avg account age), co-belonging, comment volume/post volume,
# user trajectories

with open('creds.yaml', 'r') as f:
    creds = yaml.load(f)

print(creds)    
REDDIT_ID = creds['id']
REDDIT_SECRET = creds['secret']
APP_NAME = creds['app_name']

MY_SUBREDDIT = 'wallstreetbets'
SEARCH_TERM = 'gamestop|facebook|GME'
reddit = praw.Reddit(client_id=REDDIT_ID, client_secret=REDDIT_SECRET, user_agent=APP_NAME)
subreddit = reddit.subreddit(MY_SUBREDDIT)

def get_body_wrapper(comment):
    try:
        return c.body
    except:
        return ''

def get_author_wrapper(comment):
    try:
        return c.author
    except:
        return '))NULL(('

def get_posts_over_last_n_days(reddit_instance, subreddit, search_term, n_days):
    dt_created = []
    authors = []
    num_comments_all = []
    upvote_ratios = []
    scores = []
    titles = []
    texts = []
    comments_texts_all = []
    comments_authors_all = []
    for d1 in range(2, n_days):
        d2 = d1 - 1
        res = requests.get('http://api.pushshift.io/reddit/search/submission/?q={}&subreddit={}&after={}d&before={}d&size=1000'.format(
            search_term, subreddit, str(d1), str(d2)))
        res_json = res.json()['data']
        for item in res_json:
            permalink = item['permalink']
            dt_created.append(item['created_utc'])
            authors.append(item['author'])
            num_comments_all.append(item['num_comments'])
            try:
                upvote_ratios.append(item['upvote_ratio'])
            except:
                print('no upvote ratio')
            scores.append(item['score'])
            submission = praw.models.Submission(reddit_instance, url='http://reddit.com' + permalink)
            titles.append(submission.title)
            texts.append(submission.selftext)
            comments = submission.comments.list()
            comments_authors_all.append([get_author_wrapper(c) for c in comments])
            comments_texts_all.append([get_body_wrapper(c) for c in comments])
            
            if len(dt_created) % 500 == 0:
                d = {
                    'dt_created': dt_created, 
                    'authors': authors, 
                    'num_comments_all': num_comments_all, 
                    'upvote_ratios': upvote_ratios,
                    'scores': scores,
                    'titles': titles,
                    'texts': texts,
                    'comment_texts_all': comments_texts_all,
                    'comment_authors_all': comments_authors_all
                }
                pickle.dump(d, open('reddit_info_dict_intermediate_{}.pkl'.format(str(len(dt_created))), 'wb'))
 

    d = {
         'dt_created': dt_created, 
         'authors': authors, 
         'num_comments_all': num_comments_all, 
         'upvote_ratios': upvote_ratios,
         'scores': scores,
         'titles': titles,
         'texts': texts,
         'comment_texts_all': comments_texts_all,
         'comment_authors_all': comments_authors_all
    }
    pickle.dump(d, open('reddit_info_dict_final.pkl', 'wb'))
     
get_posts_over_last_n_days(reddit, MY_SUBREDDIT, SEARCH_TERM, 10)








