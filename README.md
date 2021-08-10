# infograffiti

## To get started:
- Clone this repo (git clone ${the link you get when you click on the green button to the top right here})
- Make sure you have Python 3 installed as well as pip3.
- Install _virtualenv_: (`pip3 install virtualenv`)
- Create a new Python3 virtual environment (`virtualenv $path_to_your_environment`): for example, `virtualenv ~/alyssa/my_env`)
- Activate your virtual environment (`source $path_to_your_environment/bin/activate`): for example, `source ~/alyssa/my_env/bin/activate`)
- Install requirements in your virtual environment (`pip3 install -r requirements.txt`)

## Hello world program:
- Loosely based off of [this tutorial](https://www.storybench.org/how-to-scrape-reddit-with-python/), with expansions.
- To start off, make a reddit account if you don't have one.
- Navigate to the apps console (follow the tutorial linked above) to create your very own app.
- Put your credentials in the appropriate places in `creds.yaml`. This ensures that you won't upload your credentials to Git accidentally!
- Choose a subreddit to explore! Put its name in the appropriate place in `example.py`. 
- Add the search term. Remember, `|` means OR and `&` means AND!
- Run `example.py` and collect some data! This might take a while. 
- You can decrease the number of days you're looking at (last line of `example.py`) if you're in a hurry.
- For instructions on how to get something to run on your computer without you [jiggling the mouse](https://www.reddit.com/r/redneckengineering/comments/ob3qj9/keeping_computer_awake_while_it_compiles_code/?utm_medium=android_app&utm_source=share) every so often, try [this](https://linuxize.com/post/how-to-use-linux-screen/)
- In another window, activate your virtual environment you created previously. Launch a jupyter notebook server (`jupyter notebook`).
- In this repo, we've provided a sample data pickle file with usernames hashed for privacy; feel free to use this to play around! It contains 365 days of /r/legaladvice's mentions of any FAANG company (Facebook/Amazon/Apple/Netflix/Google).
- Take a look at dataviz.ipynb and explore the examples. What do you want to know about your data? 


