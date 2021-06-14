######################################################################
#                                                                    #
#                     Twitter Analyser                               #
#                                                                    #
#    Windows 7 32bit                          Python 3.8 32bit       #
############### Module Information ###################################
#                                                                    #
#  tweepy==3.10.0                                                    #
#  wordcloud==1.8.1                                                  #
#  pandas==1.0.1                                                     #
#  textblob                                                          #  
#                                                                    #
####################   Imports        ################################

import os
import re
import tweepy
import pandas as pd
import tkinter as tk

from textblob import TextBlob
from wordcloud import WordCloud
from tkinter import ttk,messagebox,PhotoImage,Label,Text,Frame,Button,Canvas
from PIL import ImageTk,Image
from Codes.View import Viewtweets

Version = 'V4.1'

#######################   Functions    ###############################

def login():
    'verify login into a twitter account'
    if os.path.isfile("./Settings/login.csv"):#check if csv file is present
        config = pd.read_csv("./Settings/login.csv") #read Login information from csv file
        auth = tweepy.OAuthHandler(config['twitterApiKey'][0], config['twitterApiSecret'][0])
        auth.set_access_token(config['twitterApiAccessToken'][0], config['twitterApiAccessTokenSecret'][0])
        api = tweepy.API(auth)
        try:
            test = api.verify_credentials()
            if str(test) == 'False':
                messagebox.showerror("Authentication error","Please check login.csv contents and try again !!!")
            else:
                twitterApi = tweepy.API(auth, wait_on_rate_limit = True)
                B1['state'] = 'active'
                B2['state'] = 'active'
                B3['state'] = 'active'
                messagebox.showinfo("Authentication", "Twitter Login Success")
        except:
            messagebox.showerror("login error", "Ooops.. Unable to connect twitter API's  !!!")
    else:
        messagebox.showerror("File not found error", "Please check login.csv is present in the settings folder and try again !!!")

def search(list,n):
    for i in range(len(list)):
        if list[i] == n:
            return i, True
    return i, False

def cleanUpTweet(txt):# Cleaning the tweets
    txt = re.sub(r'@[A-Za-z0-9_]+', '', txt)# Remove mentions
    txt = re.sub(r'#', '', txt)# Remove hashtags
    txt = re.sub(r'RT : ', '', txt)# Remove retweets:
    txt = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', txt)# Remove urls
    return txt

def LabelValueCorrector(Labels, Values):
    L = ["Negative", "Neutral", "Positive"]; V = [0, 0, 0]
    if len(Labels) != 0:
        for x in range(len(L)):
            index, Bool = search(Labels, L[x])
            if Bool: V[x] = Values[index]
    return L,V


def sentiment():

    def Exit_Ind():
        'back_root funtion used to close the main window'
        roots.destroy() #close the UI
        os._exit(0) #Forcefully quit python
        
    root.destroy()
    roots = tk.Tk()
    roots.title("Sentiment Analyser") #Sentiment Window Title
    roots.geometry("960x540")#1024*786 Window Size
    roots.config(bg='alice blue') # Window Bg Color http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

    def Analyze_Ind():
        CanG_S.delete("all"); CanW_S.delete("all") #Clear canvas each time.
        roots.update()
        print(individual_id.get())
        config = pd.read_csv("./Settings/login.csv")

        ##Now we need to set all Twitter API config variables required for authentication with Tweepy.

        # Twitter API config
        auth = tweepy.OAuthHandler(config['twitterApiKey'][0], config['twitterApiSecret'][0])
        auth.set_access_token(config['twitterApiAccessToken'][0], config['twitterApiAccessTokenSecret'][0])
        twitterApi = tweepy.API(auth, wait_on_rate_limit = True)

        twitterAccount = individual_id.get()

        if individual_id.get() == "":
            messagebox.showerror("Error", "Please enter an twitter ID....")
            return
        ##Now we are going to retrieve the last 50 Tweets & replies from the specified Tweeter account.
        tweets = tweepy.Cursor(twitterApi.user_timeline, 
                                screen_name=twitterAccount, 
                                count=None,
                                since_id=None,
                                max_id=None,
                                trim_user=True,
                                exclude_replies=True,
                                contributor_details=False,
                                include_entities=False
                                ).items(50);

        ##And we are going to create Pandas Data Frame from it.
        try:
            df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweet'])
        except:
            messagebox.showinfo("Error", "Please enter valid twitter ID!!!")
            return

        ##Let's see what is in the data frame by calling the head() function.
        #df.head()

        ##And nw we are going to apply it for all the Tweets in our Pandas Data Frame.
        df['Tweet'] = df['Tweet'].apply(cleanUpTweet)

        ##We are also going to build a couple more functions to calculate the subjectivity and polarity of our tweets.
        def getTextSubjectivity(txt):
            return TextBlob(txt).sentiment.subjectivity

        def getTextPolarity(txt):
            return TextBlob(txt).sentiment.polarity
    
        #print('df',df)
        ##And now we are going to apply these functions to our data frame and create two new features in our data frame Subjectivity and Polarity.
        df['Subjectivity'] = df['Tweet'].apply(getTextSubjectivity)
        df['Polarity'] = df['Tweet'].apply(getTextPolarity)
        
        #print('df polarity',df['Polarity'])

        ##Now, let's see how our data frame looks now.
        #df.head(50)

        ##The below command will remove all the rows with the Tweet column equals to "".
        df = df.drop(df[df['Tweet'] == ''].index)

        #df.head(50)

        ##Now let's build a function and categorize our tweets as Negative, Neutral and Positive.
        # negative, nautral, positive analysis
        def getTextAnalysis(a):
            if a < 0:
                return "Negative"
            elif a == 0:
                return "Neutral"
            else:
                return "Positive"

        ##And apply this functiona and create another feature in our data frame called Score.
        df['Score'] = df['Polarity'].apply(getTextAnalysis)

        ##Here is our data frame with our Tweets, Subjectivity, Polarity and Score for all our Tweets.
        #df.head(50)
        
        ##Let;s now take all positive tweets and calculate the percentage of positive tweets from all the tweets in our data frame.
        positive = df[df['Score'] == 'Positive']
        

        ##We can now visualise positive, negative, neutral tweets using Matplotlib.
        labels = df.groupby('Score').count().index.values

        values = df.groupby('Score').size().values
        
       
        labels, values = LabelValueCorrector(labels, values)
        #print(values)
 

        ##We visualise matplotlib bar graph in canvas.
        data = values
        y_stretch = 2.65; y_gap = 20
        x_stretch = 40; x_width = 80; x_gap = 50
        for x, y in enumerate(data):
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = canvas_bar_height - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = canvas_bar_height - y_gap

            if x == 0: colour = 'Red'
            elif x == 1: colour = 'Blue'
            elif x == 2: colour = 'Green'
            else: colour = 'Black'

            CanG_S.create_rectangle(x0, y0, x1, y1, fill=colour)
            CanG_S.create_text(x0+2, y0, anchor=tk.SW, text=str(y))

        
            
        ##Setting bar colours.
        Label (roots, text="Negative", bg="white", fg="black", height=1, font="none 15 bold") .place(x=70, y=480)
        Label (roots, text="Neutral", bg="white", fg="black", height=1, font="none 15 bold") .place(x=190, y=480)
        Label (roots, text="Positive", bg="white", fg="black", height=1, font="none 15 bold") .place(x=310, y=480)
        
        def display():
            Viewtweets(df)
        viewtweetui = Button(roots, text="View tweets", width=12, height=1, font="none 12 bold", command=display)
        viewtweetui.place(x=700, y=120) #button viewtweet


        objective = df[df['Subjectivity'] == 0]

        # Creating a word cloud
        words = ' '.join([tweet for tweet in df['Tweet']])
        
        wordCloud = WordCloud(width=425, height=300).generate(words)
        wordCloud.to_file(r'.\Images\Word_Cloud\Individual_Cloud.png')
        

        img = ImageTk.PhotoImage(Image.open(r'.\Images\Word_Cloud\Individual_Cloud.png'))  
        CanW_S.create_image(0, 0, anchor='nw', image=img)

        roots.mainloop()




    Frames = Frame(height = 110, width = 990, bg = 'white') #White frame to display headerimage
    Frames.place(x=0, y=0) 

    headerimages = PhotoImage(file=r'.\Images\Sentiment.gif')
    Labels = Label(roots, borderwidth = 0, relief="raised", image=headerimages)
    Labels.place(x=310, y=0, anchor='nw')#Title Image with sentiment logo

    
    Label (roots, text="Twitter ID : ", bg="white", fg="black", height=1, font="none 15 bold") .place(x=20, y=120)
   
    
    individual_id = tk.StringVar()
    Ind_List = ttk.Combobox(roots, width=15, font="none 15 bold", textvariable = individual_id)
    Ind_List['values'] = ('JoeBiden','imVkohli','barackobama','justinbieber','Cristiano','KamalaHarris','BillGates','DishPatani')
    Ind_List.place(x = 160, y = 120)

    Analyze_Btn = Button(roots, text="Analyze", width=12, height=1, font="none 12 bold", command=Analyze_Ind)
    Analyze_Btn.place(x=500, y=120) #button analyse
    
    
    ##Fixing canvas for bar graph.
    canvas_bar_width = 425; canvas_bar_height = 300
    CanG_S = tk.Canvas(roots, width=canvas_bar_width, height=canvas_bar_height, bg= 'white')
    CanG_S.place(x = 20, y = 170)

    ##Fixing canvas for word cloud.
    CanW_S = Canvas(roots, width = 425, height = 300)  
    CanW_S.place(x = 500, y = 170)

         

    Ind_Exit = Button(roots, text="Exit", width=12, height=1, font="none 15 bold", command=Exit_Ind)
    Ind_Exit.place(x=772, y=490) #button exit

    roots.mainloop()

def comparision():
    
    def Exit_Comp():
        'back_root function used to close the main window'
        rootc.destroy() #close the UI
        os._exit(0) #Forcefully quit python

    root.destroy()
    rootc = tk.Tk()
    rootc.title("Comparision") #Comparision Window Title
    rootc.geometry("960x540")#1024*786 Window Size
    rootc.config(bg='alice blue') # Window Bg Color http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

    def Analyze_Comp():

        CanG_C.delete("all"), CanG_C1.delete("all")
        winn.set('')
        rootc.update()
        
        print(comp_id1.get(), comp_id2.get())
        config = pd.read_csv("./Settings/login.csv")
        # Twitter API config
        auth = tweepy.OAuthHandler(config['twitterApiKey'][0], config['twitterApiSecret'][0])
        auth.set_access_token(config['twitterApiAccessToken'][0], config['twitterApiAccessTokenSecret'][0])
        twitterApi = tweepy.API(auth, wait_on_rate_limit = True)

        twitterAccount = comp_id1.get()# "JoeBiden"
        if comp_id1.get() == "":
            messagebox.showerror("Error", "ID1 Error\nPlease enter an twitter ID....")
            return
        
        ##Now we are going to retrieve the last 50 Tweets & replies from the specified Tweeter account.
        tweets = tweepy.Cursor(twitterApi.user_timeline, 
                                screen_name=twitterAccount, 
                                count=None,
                                since_id=None,
                                max_id=None,
                                trim_user=True,
                                exclude_replies=True,
                                contributor_details=False,
                                include_entities=False
                                ).items(50);

        ##And we are going to create Pandas Data Frame from it.
        try:
            df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweet'])
        except:
            messagebox.showinfo("Error", "ID1 Error\nPlease enter valid twitter ID!!!")
            return

        ##Let's see what is in the data frame by calling the head() function.
        #df.head()
        #print(df)
        ##Before we start our sentiment analysis it is a good idea to clean up each tweets from an unnecessary data first.
        ##We are going to create a cleanUpTweet function that will:##remove mentions##remove hashtags##remove retweets##remove urls
        

        ##And nw we are going to apply it for all the Tweets in our Pandas Data Frame.
        df['Tweet'] = df['Tweet'].apply(cleanUpTweet)

        ##We are also going to build a couple more functions to calculate the subjectivity and polarity of our tweets.
        def getTextSubjectivity(txt):
            return TextBlob(txt).sentiment.subjectivity

        def getTextPolarity(txt):
            return TextBlob(txt).sentiment.polarity

        ##And now we are going to apply these functions to our data frame and create two new features in our data frame Subjectivity and Polarity.
        df['Subjectivity'] = df['Tweet'].apply(getTextSubjectivity)
        df['Polarity'] = df['Tweet'].apply(getTextPolarity)

        ##Now, let's see how our data frame looks now.
        #df.head(50)

        ##The below command will remove all the rows with the Tweet column equals to "".
        df = df.drop(df[df['Tweet'] == ''].index)

        #df.head(50)

        ##Now let's build a function and categorize our tweets as Negative, Neutral and Positive.
        # negative, nautral, positive analysis
        def getTextAnalysis(a):
            if a < 0:
                return "Negative"
            elif a == 0:
                return "Neutral"
            else:
                return "Positive"

        ##And apply this functiona and create another feature in our data frame called Score.
        df['Score'] = df['Polarity'].apply(getTextAnalysis)

        ##Here is our data frame with our Tweets, Subjectivity, Polarity and Score for all our Tweets.#df.head(50)
        
        ##Let;s now take all positive tweets and calculate the percentage of positive tweets from all the tweets in our data frame.
        positive = df[df['Score'] == 'Positive']

        ##We can now visualise positive, negative, neutral tweets using Matplotlib.
        labels = df.groupby('Score').count().index.values

        values = df.groupby('Score').size().values

        labels, values = LabelValueCorrector(labels, values)
 
        print("Vallues one ", values[2])
        participant1 = values[2]

        ##We visualise matplotlib bar graph in canvas.
        data = values
        y_stretch = 2.65; y_gap = 20
        x_stretch = 40; x_width = 80; x_gap = 50
        for x, y in enumerate(data):
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = canvas_bar_height - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = canvas_bar_height - y_gap

            if x == 0: colour = 'Red'
            elif x == 1: colour = 'Blue'
            elif x == 2: colour = 'Green'
            else: colour = 'Black'

            CanG_C.create_rectangle(x0, y0, x1, y1, fill=colour)
            CanG_C.create_text(x0+2, y0, anchor=tk.SW, text=str(y))

        ##Setting bar colours.
        Label (rootc, text="Negative", bg="white", fg="black", height=1, font="none 12 bold") .place(x=70, y=470)
        Label (rootc, text="Neutral", bg="white", fg="black", height=1, font="none 12 bold") .place(x=195, y=470)
        Label (rootc, text="Positive", bg="white", fg="black", height=1, font="none 12 bold") .place(x=315, y=470)


        objective = df[df['Subjectivity'] == 0]

        #twitterAccount = "JoeBiden"
        twitterAccount = comp_id2.get()
        if comp_id2.get() == "":
            messagebox.showerror("Error", "ID2 Error\nPlease enter an twitter ID....")
            return
        
        ##Now we are going to retrieve the last 50 Tweets & replies from the specified Tweeter account.
        tweets = tweepy.Cursor(twitterApi.user_timeline, 
                                screen_name=twitterAccount, 
                                count=None,
                                since_id=None,
                                max_id=None,
                                trim_user=True,
                                exclude_replies=True,
                                contributor_details=False,
                                include_entities=False
                                ).items(50);

        ##And we are going to create Pandas Data Frame from it.
        try:
            df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweet'])
        except:
            messagebox.showinfo("Error", "ID2 Error\nPlease enter valid twitter ID!!!")
            return


        ##And nw we are going to apply it for all the Tweets in our Pandas Data Frame.
        df['Tweet'] = df['Tweet'].apply(cleanUpTweet)

        ##We are also going to build a couple more functions to calculate the subjectivity and polarity of our tweets.
        def getTextSubjectivity(txt):
            return TextBlob(txt).sentiment.subjectivity

        def getTextPolarity(txt):
            return TextBlob(txt).sentiment.polarity

        ##And now we are going to apply these functions to our data frame and create two new features in our data frame Subjectivity and Polarity.
        df['Subjectivity'] = df['Tweet'].apply(getTextSubjectivity)
        df['Polarity'] = df['Tweet'].apply(getTextPolarity)

        ##Now, let's see how our data frame looks now.
        #df.head(50)

        ##The below command will remove all the rows with the Tweet column equals to "".
        df = df.drop(df[df['Tweet'] == ''].index)

        #df.head(50)

        ##Now let's build a function and categorize our tweets as Negative, Neutral and Positive.
        # negative, nautral, positive analysis
        def getTextAnalysis(a):
            if a < 0:
                return "Negative"
            elif a == 0:
                return "Neutral"
            else:
                return "Positive"

        ##And apply this functiona and create another feature in our data frame called Score.
        df['Score'] = df['Polarity'].apply(getTextAnalysis)

        ##Here is our data frame with our Tweets, Subjectivity, Polarity and Score for all our Tweets.
        #df.head(50)
        
        ##Let;s now take all positive tweets and calculate the percentage of positive tweets from all the tweets in our data frame.
        positive = df[df['Score'] == 'Positive']

        ##We can now visualise positive, negative, neutral tweets using Matplotlib.
        labels = df.groupby('Score').count().index.values

        values = df.groupby('Score').size().values
        
        labels, values = LabelValueCorrector(labels, values)
        print("Vallues two ", values[2])
        
        participant2 = values[2]
        #Finding the Winner 
        if participant1 > participant2:
            winn.set('Winner is ' + comp_id1.get())
        elif participant1 == participant2:
            winn.set('Oh It is a Tie')
        else:
            winn.set('Winner is ' + comp_id2.get())
            
            
            
        ##We visualise matplotlib bar graph in canvas.
        data = values
        y_stretch = 2.65; y_gap = 20
        x_stretch = 40; x_width = 80; x_gap = 50
        for x, y in enumerate(data):
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = canvas_bar_height - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = canvas_bar_height - y_gap

            if x == 0: colour = 'Red'
            elif x == 1: colour = 'Blue'
            elif x == 2: colour = 'Green'
            else: colour = 'Black'

            CanG_C1.create_rectangle(x0, y0, x1, y1, fill=colour)
            CanG_C1.create_text(x0+2, y0, anchor=tk.SW, text=str(y))

        ##Setting bar colours.
        Label (rootc, text="Negative", bg="white", fg="black", height=1, font="none 12 bold") .place(x=555, y=470)
        Label (rootc, text="Neutral", bg="white", fg="black", height=1, font="none 12 bold") .place(x=675, y=470)
        Label (rootc, text="Positive", bg="white", fg="black", height=1, font="none 12 bold") .place(x=795, y=470)


        objective = df[df['Subjectivity'] == 0]

        win_label = Label(rootc, textvariable=winn, bg="white", fg="green", height=1, font="none 15 bold")
        win_label.place(x=370, y=500)
        
        rootc.mainloop()


    
    Framec = Frame(height = 110, width = 990, bg = 'white') #White frame to display headerimage
    Framec.place(x=0, y=0) 

    headerimagec = PhotoImage(file=r'.\Images\Comparision.gif')
    Labelc = Label(rootc, borderwidth = 0, relief="raised", image=headerimagec)
    Labelc.place(x=310, y=0, anchor='nw')#Title Image with comparision LOGO

    Label (rootc, text="Twitter IDs : ", bg="white", fg="black", height=1, font="none 15 bold") .place(x=20, y=120)


    comp_id1 = tk.StringVar()
    comp_id2 = tk.StringVar()
    winn = tk.StringVar()
    Comp1_List = ttk.Combobox(rootc, width=15, font="none 15 bold", textvariable = comp_id1)
    Comp1_List['values'] = ('netflix','amazonprimenow','DisneyPlusHS','Flipkart','CovaxinVaccine','GooglePay','amazon','Covishield','NPCI_BHIM')
    Comp1_List.place(x = 160, y = 120)
    Comp2_List = ttk.Combobox(rootc, width=15, font="none 15 bold", textvariable = comp_id2)
    Comp2_List['values'] = ('GooglePay','Covishield','amazon','netflix','CovaxinVaccine','amazonprimenow','DisneyPlusHS','Flipkart','NPCI_BHIM')
    Comp2_List.place(x = 350, y = 120)

    Analyze_Btn = Button(rootc, text="Compare", width=12, height=1, font="none 12 bold", command=Analyze_Comp)
    Analyze_Btn.place(x=540, y=120) #button compare

    
    ##Fixing canvas for bar graphs.
    canvas_bar_width = 425; canvas_bar_height = 300
    CanG_C = tk.Canvas(rootc, width=canvas_bar_width, height=canvas_bar_height, bg= 'white')
    CanG_C.place(x = 20, y = 170)

    canvas_bar_width1 = 425; canvas_bar_height1 = 300
    CanG_C1 = tk.Canvas(rootc, width=canvas_bar_width1, height=canvas_bar_height1, bg= 'white')
    CanG_C1.place(x = 500, y = 170)

    Comp_Exit = Button(rootc, text="Exit", width=12, height=1, font="none 15 bold", command=Exit_Comp)
    Comp_Exit.place(x=772, y=495) #button exit

    rootc.mainloop()


def hashtag():
    
    def Exit_Hash():
        'back_root function used to close the main window'
        rooth.destroy() #close the UI
        os._exit(0) #Forcefully quit python

    root.destroy()
    rooth = tk.Tk()
    rooth.title("Hashtag") #Hashtag Window Title
    rooth.geometry("960x540")#1024*786 Window Size
    rooth.config(bg='alice blue') # Window Bg Color http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

    def Analyze_Hash():

        CanG_H.delete("all"), CanW_H.delete("all")
        rooth.update()
        
        def scrape(words, numtweet):
            # Creating DataFrame using pandas
            db = pd.DataFrame(columns=['username', 'description', 'location', 'following',
                                                            'followers', 'totaltweets', 'retweetcount', 'Tweet', 'hashtags'])
            # We are using .Cursor() to search through twitter for the required tweets.
            # The number of tweets can be restricted using .items(number of tweets)
            tweets = tweepy.Cursor(api.search, q=words, lang="en", tweet_mode='extended').items(numtweet)#since=date_since
            
            # .Cursor() returns an iterable object. Each item in
            # the iterator has various attributes that you can access to
            # get information about each tweet
            list_tweets = [tweet for tweet in tweets]
            
            # Counter to maintain Tweet Count
            i = 1
                
            # we will iterate over each tweet in the list for extracting information about each tweet
            for tweet in list_tweets:
                username = tweet.user.screen_name
                description = tweet.user.description
                location = tweet.user.location
                following = tweet.user.friends_count
                followers = tweet.user.followers_count
                totaltweets = tweet.user.statuses_count
                retweetcount = tweet.retweet_count
                hashtags = tweet.entities['hashtags']
                
                # Retweets can be distinguished by a retweeted_status attribute,
                # in case it is an invalid reference, except block will be executed
                try:
                    text = tweet.retweeted_status.full_text
                except AttributeError:
                    text = tweet.full_text
                hashtext = list()
                for j in range(0, len(hashtags)):
                    hashtext.append(hashtags[j]['text'])
                # Here we are appending all the extracted information in the DataFrame
                ith_tweet = [username, description, location, following, followers, totaltweets, retweetcount, text, hashtext]
                db.loc[len(db)] = ith_tweet
                # Function call to print tweet data on screen
                i = i+1
            db.to_csv('./Images/temp/scraped_tweets.csv')
        
        #print(Hashtags.get())
        if Hashtags.get() == "":
            messagebox.showerror("Error", "Please enter hashtag....")
            return
        
        # Twitter API config
        config = pd.read_csv("./Settings/login.csv")
        auth = tweepy.OAuthHandler(config['twitterApiKey'][0], config['twitterApiSecret'][0])
        auth.set_access_token(config['twitterApiAccessToken'][0], config['twitterApiAccessTokenSecret'][0])
        api = tweepy.API(auth)
        scrape(Hashtags.get(), 100) # 100 is number of tweet

        def filter_columns(filename):
            ''' This will filter the columns in reqlst in the csv file '''
            data_frame = pd.read_csv(filename, low_memory=False, error_bad_lines=False)
            reqlst = [8] #Filter column Tweet from CSV file Delete all others
            final_df = data_frame.iloc[:, reqlst]
            final_df.to_csv(filename, index=False)

        filter_columns('./Images/temp/scraped_tweets.csv')#Filter unwanted columns in csv data
        df = pd.read_csv('./Images/temp/scraped_tweets.csv')#Read Dataframe from csv
        #print(df)

        ##And nw we are going to apply it for all the Tweets in our Pandas Data Frame.
        df['Tweet'] = df['Tweet'].apply(cleanUpTweet)

        ##We are also going to build a couple more functions to calculate the subjectivity and polarity of our tweets.
        def getTextSubjectivity(txt):
            return TextBlob(txt).sentiment.subjectivity

        def getTextPolarity(txt):
            return TextBlob(txt).sentiment.polarity

        ##And now we are going to apply these functions to our data frame and create two new features in our data frame Subjectivity and Polarity.
        df['Subjectivity'] = df['Tweet'].apply(getTextSubjectivity)
        df['Polarity'] = df['Tweet'].apply(getTextPolarity)

        ##Now, let's see how our data frame looks now.
        #df.head(50)

        ##The below command will remove all the rows with the Tweet column equals to "".
        df = df.drop(df[df['Tweet'] == ''].index)

        #df.head(50)

        ##Now let's build a function and categorize our tweets as Negative, Neutral and Positive.
        # negative, nautral, positive analysis
        def getTextAnalysis(a):
            if a < 0:
                return "Negative"
            elif a == 0:
                return "Neutral"
            else:
                return "Positive"

        ##And apply this functiona and create another feature in our data frame called Score.
        df['Score'] = df['Polarity'].apply(getTextAnalysis)

        ##Here is our data frame with our Tweets, Subjectivity, Polarity and Score for all our Tweets.
        #df.head(50)

        ##Let;s now take all positive tweets and calculate the percentage of positive tweets from all the tweets in our data frame.
        positive = df[df['Score'] == 'Positive']

        print(str(positive.shape[0]/(df.shape[0])*100) + " % of positive tweets")

        ##We can now visualise positive, negative, neutral tweets using Matplotlib.
        labels = df.groupby('Score').count().index.values

        values = df.groupby('Score').size().values        
       
        labels, values = LabelValueCorrector(labels, values)

        ##We visualise matplotlib bar graph in canvas.
        data = values
        y_stretch = 2.65; y_gap = 20
        x_stretch = 40; x_width = 80; x_gap = 50
        for x, y in enumerate(data):
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = canvas_bar_height - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = canvas_bar_height - y_gap

            if x == 0: colour = 'Red'
            elif x == 1: colour = 'Blue'
            elif x == 2: colour = 'Green'
            else: colour = 'Black'

            CanG_H.create_rectangle(x0, y0, x1, y1, fill=colour)
            CanG_H.create_text(x0+2, y0, anchor=tk.SW, text=str(y))

        ##Setting bar colours.
        Label (rooth, text="Negative", bg="white", fg="black", height=1, font="none 15 bold") .place(x=70, y=480)
        Label (rooth, text="Neutral", bg="white", fg="black", height=1, font="none 15 bold") .place(x=190, y=480)
        Label (rooth, text="Positive", bg="white", fg="black", height=1, font="none 15 bold") .place(x=310, y=480)

        def display():
            Viewtweets(df)
        viewtweetui = Button(rooth, text="View tweets", width=12, height=1, font="none 12 bold", command=display)
        viewtweetui.place(x=700, y=120) #button viewtweet


        objective = df[df['Subjectivity'] == 0]

        # Creating a word cloud
        words = ' '.join([tweet for tweet in df['Tweet']])
        
        wordCloud = WordCloud(width=425, height=300).generate(words)
        wordCloud.to_file(r'./Images/Word_Cloud/Hastag_Cloud.png')
                            
        img = ImageTk.PhotoImage(Image.open(r'./Images/Word_Cloud/Hastag_Cloud.png'))  
        CanW_H.create_image(0, 0, anchor='nw', image=img)

        rooth.mainloop()


    Frameh = Frame(height = 103, width = 990, bg = 'white') #White frame to display headerimage
    Frameh.place(x=0, y=0) 

    headerimageh = PhotoImage(file=r'.\Images\Hashtag.gif')
    Labelh = Label(rooth, borderwidth = 0, relief="raised", image=headerimageh)
    Labelh.place(x=260, y=0, anchor='nw')#Title Image with hashtag LOGO

    Label (rooth, text="Hashtag # : ", bg="white", fg="black", height=1, font="none 15 bold") .place(x=20, y=120)
   
    Hashtags = tk.StringVar()
    Hash_List = ttk.Combobox(rooth, width=24, font="none 15 bold", textvariable = Hashtags)
    Hash_List['values'] = ('DMK','admk','bjp','IndiaFightsCorona','COVID19','ThankYouCoronaWarriors')
    Hash_List.place(x = 160, y = 120)

    Analyze_Btn = Button(rooth, text="Analyze", width=12, height=1, font="none 12 bold", command=Analyze_Hash)
    Analyze_Btn.place(x=500, y=120) #button analyse
    
    canvas_bar_width = 425; canvas_bar_height = 300 ##Fixing canvas for bar graph.
    CanG_H = tk.Canvas(rooth, width=canvas_bar_width, height=canvas_bar_height, bg= 'white')
    CanG_H.place(x = 20, y = 170)
    CanW_H = Canvas(rooth, width = 425, height = 300)##Fixing canvas for word cloud.
    CanW_H.place(x = 500, y = 170)

    Hash_Exit = Button(rooth, text="Exit", width=12, height=1, font="none 15 bold", command=Exit_Hash)
    Hash_Exit.place(x=772, y=490) #button exit
    
    rooth.mainloop()
    
#######################################
    
def close_root():
    'close-root function close the program'
    root.destroy() #close the UI
    os._exit(0) #Forcefully quit python


root = tk.Tk()
root.title("Twitter Analyser" + "_" + Version) #Main Window Title
root.geometry("960x540")#1024*786 Window Size
root.config(bg='alice blue') # Window Bg Color http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

Frame1 = Frame(height = 105, width = 990, bg = 'white') #White frame
Frame1.place(x=0, y=0) 

headerimage = PhotoImage(file=r'.\Images\Label.gif')
Label1 = Label(root, borderwidth = 0, relief="raised", image=headerimage)
Label1.place(x=310, y=0, anchor='nw')#Title Image with twitter LOGO

Label (root, text="Click Here to Login : ", bg="white", fg="black", height=2, font="none 15 bold") .place(x=100, y=150)

Login_Btn = Button(root, text="LOGIN", width=12, height=2, font="none 15 bold", command=login)
Login_Btn.place(x=350, y=150)
Main_Exit = Button(root, text="EXIT", width=12, height=1, font="none 15 bold", command=close_root)
Main_Exit.place(x=790, y=490)
B1 = Button(root, text="Individual", width=14, height=2, font="none 15 bold", command=sentiment)
B1.place(x=100, y=350)
B2 = Button(root, text="Comparision", width=14, height=2, font="none 15 bold", command=comparision)
B2.place(x=350, y=350)
B3 = Button(root, text="Hashtag", width=14, height=2, font="none 15 bold", command=hashtag)
B3.place(x=600, y=350)

B1['state'] = 'disable'
B2['state'] = 'disable'
B3['state'] = 'disable'





root.mainloop()
