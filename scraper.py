# Twitter scraper

import csv
import tweepy

username = ''
users_export_path = ''
tweets_export_path = ''

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


def fetch_followed(screen_name):
    # returns ids of accounts followed by username
    print('\nFetching accounts followed by %s...' % screen_name)
    followed_ids = api.friends_ids(screen_name)
    print('Returned %s accounts.' % len(followed_ids))
    return followed_ids


def fetch_user_tweets(user_id):
    # returns max number of tweets allowed by api (3200) for id
    print('\nFetching tweets...')

    # intial request
    all_tweets = []
    new_tweets = api.user_timeline(id=user_id, count=200, include_rts=True, wait_on_rate_limit=True, wait_one_wait_limit_notify=True)
    all_tweets.extend(new_tweets)
    bookmark = all_tweets[-1].id - 1

    # follow-up requests
    request_count = 1
    while len(new_tweets) > 0:
        request_count += 1
        new_tweets = api.user_timeline(id=user_id, count=200, include_rts=True, max_id=bookmark, wait_on_rate_limit=True, wait_one_wait_limit_notify=True)
        all_tweets.extend(new_tweets)
        bookmark = all_tweets[-1].id - 1

    name = all_tweets[0].user.name
    screen_name = all_tweets[0].user.screen_name
    print('Returned %s tweets from %s (%s).' % (len(all_tweets), name, screen_name))
    return all_tweets


if __name__ == '__main__':

    followed_ids = fetch_followed(username)
    followed_tweets = []
    for i in range(len(followed_ids)):
        tweets = fetch_user_tweets(followed_ids[i])
        followed_tweets.append(tweets)

    tweets = []
    users = []
    for i in range(len(followed_tweets)):
        users.append([
            followed_tweets[i][0].user.id,
            followed_tweets[i][0].user.name.encode("utf-8"),
            followed_tweets[i][0].user.screen_name.encode("utf-8"),
            followed_tweets[i][0].user.description.encode("utf-8"),
            followed_tweets[i][0].user.created_at,  # utc
            followed_tweets[i][0].user.location.encode("utf-8"),
            followed_tweets[i][0].user.followers_count,
            followed_tweets[i][0].user.friends_count,
            followed_tweets[i][0].user.statuses_count,
        ])
        for j in range(len(followed_tweets[i])):
            tweets.append([
                followed_tweets[i][j].id,
                followed_tweets[i][j].user.id,
                followed_tweets[i][j].created_at,  # utc
                followed_tweets[i][j].text.encode("utf-8"),
                followed_tweets[i][j].retweet_count,
                followed_tweets[i][j].favorite_count,
                followed_tweets[i][j].in_reply_to_screen_name
            ])

    with open(users_export_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow([
            'id',
            'name',
            'screen_name',
            'bio',
            'created_at',
            'location',
            'follower_count',
            'friend_count',
            'status_count'
        ])
        writer.writerows(users)

    with open(tweets_export_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow([
            'id',
            'user_id',
            'created_at',
            'text',
            'retweet_count',
            'favorite_count',
            'in_reply_to_screen_name'
        ])
        writer.writerows(tweets)

    print("\nFiles saved.")

