# twitter-scraper

The scraper requires twitter api access. It is also restricted by an api rate limit and tweet limit per user (3200). Scraper waits on rate limit and continues once lifted.

Retrieves the following user information:
- id
- name
- screen name
- description
- account creation datetime
- location
- user follower count
- user followed-by count ("friends" count)

Retrieves the following tweet information:
- id
- user id
- tweet datetime
- tweet text
- retweet count
- favorite count
- replied-to screen name, if relevant
