from fastapi import FastAPI
import mlflow
import re
import uvicorn
import re
import pickle

#loading the english language small model of spacy
#en = spacy.load('en_core_web_sm')

#en = spacy.load('en_core_web_sm')
stopwords = ['anyone',
 'hereafter',
 'n‘t',
 'been',
 'where',
 'i',
 'nobody',
 'except',
 'anything',
 'could',
 'through',
 'back',
 'twenty',
 'me',
 'around',
 'anywhere',
 'themselves',
 'often',
 'however',
 'see',
 'by',
 'last',
 'under',
 'off',
 'otherwise',
 'therefore',
 'during',
 'my',
 'she',
 "'d",
 'within',
 'each',
 'these',
 '‘m',
 'front',
 'mostly',
 'among',
 'eight',
 'somehow',
 'whole',
 '‘d',
 'this',
 'show',
 'much',
 'once',
 'against',
 're',
 'though',
 'everything',
 'hence',
 'that',
 'everyone',
 'very',
 'into',
 'whether',
 'call',
 'can',
 'make',
 'have',
 'others',
 'something',
 'third',
 'those',
 'thence',
 'via',
 'amongst',
 'will',
 'it',
 'herein',
 'least',
 'had',
 'thereupon',
 'its',
 'either',
 'doing',
 'latter',
 'sometime',
 'cannot',
 'or',
 'nevertheless',
 'next',
 'seemed',
 'hereupon',
 'which',
 'of',
 'although',
 'three',
 'most',
 'nowhere',
 'several',
 'who',
 'empty',
 'before',
 'too',
 'fifteen',
 '‘s',
 'everywhere',
 "'ll",
 'less',
 'quite',
 'throughout',
 'meanwhile',
 'about',
 'almost',
 'on',
 'they',
 'made',
 'her',
 'yourself',
 'else',
 'former',
 'another',
 "'re",
 'only',
 '’s',
 '’re',
 'someone',
 '’m',
 'whereby',
 'yours',
 'few',
 'name',
 'ours',
 'after',
 'without',
 'well',
 'ten',
 'may',
 'latterly',
 'itself',
 'becoming',
 'your',
 '‘ll',
 'am',
 'move',
 'together',
 'hers',
 'whence',
 'also',
 '’d',
 'eleven',
 'take',
 'his',
 'therein',
 'do',
 'keep',
 'below',
 'we',
 'side',
 'please',
 'due',
 '’ve',
 'yet',
 'to',
 'become',
 'being',
 'the',
 'rather',
 'more',
 'up',
 'becomes',
 'thru',
 'besides',
 'various',
 'but',
 'nor',
 'anyhow',
 '‘re',
 'full',
 'again',
 'then',
 'beforehand',
 'wherein',
 'any',
 'be',
 'ourselves',
 'us',
 'neither',
 'nothing',
 'there',
 'two',
 'has',
 'enough',
 'own',
 'put',
 'serious',
 'n’t',
 'you',
 'how',
 'above',
 'he',
 'what',
 'sixty',
 'elsewhere',
 'over',
 'an',
 'because',
 'now',
 'other',
 'alone',
 'ca',
 'down',
 'a',
 'their',
 'always',
 'might',
 'hereby',
 '’ll',
 'since',
 'some',
 'bottom',
 'upon',
 'six',
 'if',
 'afterwards',
 'done',
 'moreover',
 'would',
 'thus',
 'part',
 'first',
 'somewhere',
 'mine',
 'sometimes',
 'give',
 'namely',
 'fifty',
 'did',
 'whither',
 'behind',
 'twelve',
 'whatever',
 'never',
 'whom',
 'so',
 'for',
 'him',
 'whenever',
 'every',
 'say',
 "'m",
 'does',
 'unless',
 'formerly',
 'beside',
 'here',
 'none',
 'himself',
 'regarding',
 'was',
 "n't",
 'across',
 'should',
 'amount',
 'are',
 'herself',
 'get',
 'wherever',
 'per',
 'from',
 'five',
 'whereupon',
 'yourselves',
 'perhaps',
 'when',
 'forty',
 "'ve",
 'toward',
 'indeed',
 'towards',
 'noone',
 'at',
 'in',
 'while',
 'along',
 'onto',
 'whose',
 "'s",
 'both',
 'hundred',
 'whereafter',
 'why',
 'seeming',
 'were',
 'used',
 'must',
 'them',
 'became',
 'go',
 'still',
 'many',
 'ever',
 'one',
 'seems',
 'seem',
 'thereby',
 'thereafter',
 'between',
 'all',
 'not',
 'beyond',
 'whoever',
 'using',
 'as',
 'our',
 'further',
 '‘ve',
 'than',
 'really',
 'out',
 'myself',
 'no',
 'top',
 'same',
 'anyway',
 'nine',
 'until',
 'just',
 'with',
 'and',
 'whereas',
 'is',
 'already',
 'such',
 'four',
 'even']


def preprocess_tweet(tweet):
    #Preprocess the text in a single tweet
    #arguments: tweet = a single tweet in form of string 
    #convert the tweet to lower case
    tweet.lower()
    #convert all urls to sting "URL"
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #convert all @username to "AT_USER"
    tweet = re.sub('@[^\s]+','AT_USER', tweet)
    #correct all multiple white spaces to a single white space
    tweet = re.sub('[\s]+', ' ', tweet)
    #convert "#topic" to just "topic"
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #remove_tags
    tweet = re.sub('<.*?>','',tweet)
    tweet = re.sub(r'@\w+', '', tweet)
    
    words = tweet.split() 
    clean_words = [word for word in words if (word not in stopwords) and len(word) > 1] 
    tweet =  " ".join(clean_words) 
    
    return tweet

# load pickle
tfidf_vectorizer = pickle.load(open("tfidf_vectorizer.pickle", "rb"))

model_path = "mlruns/1/52f9af789a36475cac1b2e04e8895d60/artifacts/model"
model = mlflow.pyfunc.load_model(model_path)

app = FastAPI()


@app.post("/predict")
def predict(input_tweet):
    # Preprocess the text
    
    input_tweet_preprocessed = preprocess_tweet(input_tweet)
    
    features_tweet = tfidf_vectorizer.transform([input_tweet_preprocessed])
    
    # Make the prediction using the trained model
    prediction = model.predict(features_tweet)
    
    # Return the prediction as a string
    return {'input_tweet': input_tweet, 'input_tweet_preprocessed':input_tweet_preprocessed, "prediction": "positive" if prediction == 4 else "negative"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

#    