ROBOT
=====
Reddit Observation Bot On Twitch

This is a multifunctional Twitch bot that has meaningful and engaging interactions with its users.

Its mission is to recognize a chat's sentiment, entertain users within the chat accordingly, and promote both collaborative and competitive activity within the chat.

Recognizing a Chat's sentiment
----------------------------
The bot stores and analyzes recent chat messages for reoccuring emotes. Upon request, it posts the most popular emote of a certain time interval, which allows users to reflect upon the chat's hivemind and contribute their own 28-pixel creative expression. Chat activity and sentiment is used to adjust the bot's actions within the chat.

Entertaining Users
------------------
The bot uses Reddit to crowdsource artificially intelligent conversations. For example, it tells mystifying riddles that the community finds the most bemusing, breaking news that the community finds the most relevant, and hilarious jokes that the community finds the most humorous. These are the most agreed-with and conversation-provoking posts on Reddit, and we believe that Twitch may find these posts just as intriguing.

Promoting Activity
------------------
The bot promotes activity within the chat by raising challenges and contests on regular intervals. The bot currently has functionality to ask riddles and host typing contests. Riddles from the most thought-provoking posts from Reddit are asked, and the bot notifies users if they have correctly answered the riddle. It also hosts a typing contest, where one sentence is posted and the first user to correctly copy the sentence into the chat is congratulated and ranked in a leaderboard.

Using the Bot
-------------
The user types `!menu` to see a privately-messaged list of available commands.

`!typerace` creates a typerace and posts the winner on a leaderboard.

`!leaderboard` shows the leaderboard from !typerace.

`!jokes` tells a top joke from Reddit.

`!riddle` asks a top riddle from Reddit and checks the chat for an answer.

`!news` posts breaking news from Reddit.

`!emotepulse` shows the hottest emote in a chat.

Notes
-----
* Jokes and riddles are filtered for offensive content that does not abide by Twitch's Rules of Conduct.

* News posts, however, are intentionally sourced from uncensored Reddit posts to promote freedom of information.

* Typerace phrases are useful tips scraped from Reddit's YouShouldKnow subreddit, which allows users to learn as they type. The phrases are posted in Unicode Mathematical Alphanumeric Symbols and analyzed in Latin symbols to prevent copying and pasting.
