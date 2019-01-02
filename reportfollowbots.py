#!/usr/bin/env python3
#
# Find the bots following a Twitter account and report them
#
# http://docs.tweepy.org/en/v3.6.0/api.html

import tweepy
import time

# Set this to the account that has a lot of fake followers
ACCOUNT_TARGET = '@usernamegoeshere'

# Twitter is not very transparent about what the reporting limit is.
# Through experience, I believe it's 49 per day.
REPORTING_LIMIT = 49

# Sample some follow-bot accounts and set these to taste
MIN_FOLLOWERS = 2
MIN_FOLLOWING = 25
MIN_TWEETS = 1

# Your authentication stuff goes here
consumerkey = 'your consumer key goes here'
consumersecret = 'your secret consumer key goes here'
accesstoken = 'your access token goes here'
accesstokensecret = 'your secret access token goes here'

auth = tweepy.OAuthHandler(consumerkey, consumersecret)
auth.set_access_token(accesstoken, accesstokensecret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

print('Find the bots following an account and report them.')
print('Allow this to run for a long time; Twitter allows 15 API calls per 15 minutes.')

followersProcessed = 0
spammersFound = 0
batchNumber = 1

while spammersFound < REPORTING_LIMIT:

        # Get another batch of followers.
        followers = api.followers(ACCOUNT_TARGET)

        print("Batch #" + str(batchNumber))

        for follower in followers:
                
                # Do they have few followers?
                fewFollowers = follower.followers_count < MIN_FOLLOWERS

                # Do they follow few others?
                fewFollowing = follower.friends_count < MIN_FOLLOWING

                # How many tweets have they tweeted?
                fewTweeets = follower.statuses_count < MIN_TWEETS

                # Get their screen name
                screenName = follower.screen_name

                # Get their user ID in case we will report them to Twitter
                userID = follower.id_str

                # Check to see if this is a spammer.
                followerIsSpammer = fewFollowers and fewFollowing and fewTweeets

                # If so, report them.
                if followerIsSpammer:
                        spammersFound = spammersFound + 1

                        print("Found spammer #" + str(spammersFound) +  ": twitter.com/" + screenName)
                        
                        api.report_spam(userID)

                followersProcessed = followersProcessed + 1
                
        print ("Processed " + str(followersProcessed) + " followers. About to request another batch...\n")
        batchNumber = batchNumber + 1
        time.sleep(60)

print('Done.')
