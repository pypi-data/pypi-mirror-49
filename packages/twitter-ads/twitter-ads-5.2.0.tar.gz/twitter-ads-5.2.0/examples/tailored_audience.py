from twitter_ads.client import Client
from twitter_ads.audience import TailoredAudience

CONSUMER_KEY = 'ozoJ1NKJg4etRJeStM07BQxRs'
CONSUMER_SECRET = 'm8tk55tqC9RiYOAlzxxLwOMjb7oFWuvTT0tpJXWrB2XfHx3gLV'
ACCESS_TOKEN = '95490672-JnxdMfGUEcuNtnbkrIAGZfthUEZkeYPE6oHVYj9qS'
ACCESS_TOKEN_SECRET = 'zPR5bWyfVyXnSqouOFRiKvp2sC36dFcYt9TXtJiGeT5tO'
ACCOUNT_ID = '18ce54t1ol3'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# create a new tailored audience
audience = TailoredAudience.all(account)

print(audience)

for i in audience:
    print(i)