# cenz_io, the multi functional twitter bot

*cenz_io* allows you to create a twitter bots that do what you want them to do with ease. The bot is built on top of the python library tweepy which is used to interact with twitter's API. What I tried to do to separate this bot from others that already exist, is allow the user to run multiple different bots on different accounts within the same program.

## Goals to accomplish before the bot goes live

+ Although not finished at this moment of time, there is a class *BotManager* that will handle running all the bots based on each bots configuration without having any user interference.

+ Give users the decision to configure the bot(s) via code and via configuration file. The philosphy of the bot is to be as simple as possible so that anyone, including non programmers can get one up and running.

+ Rate limit awareness. All bots will api rate limit aware, and won't discard data if they can't complete their duties. Bot's will have the ability to know which specifc parts of the api have reach their rate limit and will hold off on their duties until they have given more api calls.

+ Scheduling bots to run at a specific time. This feature will most likely be implemented within the bot manager, but it will allow the bot to be active for specfic times of the day. When a bot goes inactive it will continue to wherever it had left off before.


## Dependencies

+ tweepy