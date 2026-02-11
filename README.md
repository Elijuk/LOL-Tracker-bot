# League of Legends Tracker for Discord

A useful Discord bot that allows you and your friends to track your League of Legends games directly from within your Discord client.


## Description

The privileged users can add people to a tracker-system, which the bot uses to fetch data using Riot's API for this user. The bot will then automatically detect when this user has played a match of League of Legends, and automatically send a recap / overview in the desired channel.


## Intended Usage

This project is designed to be self-hosted for personal or small community use. It is provided as a base for running your own private League tracking tools.

It is not intended to be run as a public service or a large-scale hosted bot. Each user should obtain their own Personal Riot API key and respect [Riot Games' Developer Policies and rate limitst](https://developer.riotgames.com/docs/portal)

When forking or modifyuing the project, please keep credit to the original repository.


### Dependencies

* Python 3.10+
* discord.py
* python-dotenv
* pillow
* aiohttp


### Installing

1. Clone the repository:
   ```
   git clone https://github.com/xShive/LoL-Tracker-for-Discord.git
   ```

2. Create a .env file in the root folder:
    ```
    DISCORD_TOKEN="token"
    RIOT_TOKEN="token"
    DEV_IDS="123,456,789"
    ```

3. Install dependencies


### Author

Shive


### Note

Bot is still under development. Requires a self-hosted server.
Thanks for the tracker, HinTrill.

