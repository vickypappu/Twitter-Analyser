import pandas as pd


def filter_columns(filename):
    ''' This will filter the columns in reqlst in the csv file '''
    data_frame = pd.read_csv(filename, low_memory=False, error_bad_lines=False)
    reqlst = [8]
    final_df = data_frame.iloc[:, reqlst]
    final_df.to_csv(filename, index=False)

filter_columns('scraped_tweets.csv')

print('Done...')



df = pd.read_csv('scraped_tweets.csv')

print(df) 
