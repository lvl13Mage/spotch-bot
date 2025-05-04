---
sidebar_position: 1
---

# Tutorial

Let's setup Spotch Bot together!

## Installation

Download the latest version of Spotch Bot from Releases:\
[Releases](https://github.com/lvl13Mage/spotch-bot/tags)

We support Linux and Windows.

Extract the ZIP Contents into a Directory of your choice.

## Starting the Bot

Execute the File in the directory to start the Spotch Bot. 

I will open a Terminal Window and your Browser with a new Tab. 

:::note
In future Releases, we may get rid of the Terminal Window.
:::
![img alt](/img/tutorial/spotchbot-firstpage.png)

## Configuration

For Spotch Bot to work, you need to setup a Spotify Developer App and a Twitch Developer App.

### Spotify Developer App Setup

1. Naviate to the Spotify Settings in Spotch Bot.
![img alt](/img/tutorial/spotch-spotify-setup.png)

2. Visit the Spotify Developer Website and Login:
[https://developer.spotify.com/](https://developer.spotify.com/)

3. Once logged in, go to the dashboard:
[https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)

4. Then click "Create app"
![img alt](/img/tutorial/spotify-dev-creation1.png)

5. Fill the information\
⚠️ Make sure to fill the "Redirect URI" with the URI from Step 1
![img alt](/img/tutorial/spotify-dev-creation2.png)

6. Copy the Client ID and the Client Secret into the Spotch Bot app
![img alt](/img/tutorial/spotify-dev-creation3.png)
![img alt](/img/tutorial/spotify-dev-creation4.png)

7. Click Save and then Authenticate in the Spotch App\
A new Tab should open and ask for Permission.\
Once accepted you should see this:\
```{"Token received":true}```

Your Spotify App is now Authenticated!

### Twitch Developer App Setup

1. Naviate to the Twitch Settings in Spotch Bot.
![img alt](/img/tutorial/spotch-twitch-setup.png)

2. Visit the Twitch Developer Website and Login:
[https://dev.twitch.tv/](https://dev.twitch.tv/)

3. Once logged in, go to the console -> Applications Area:
[https://dev.twitch.tv/console/apps](https://dev.twitch.tv/console/apps)

4. Then click "+ Register Your Application"
![img alt](/img/tutorial/twitch-dev-create.png)

5. Fill the information\
⚠️ Make sure to fill the "Redirect URI" with the URI from Step 1
![img alt](/img/tutorial/twitch-dev-create2.png)

6. When the app is created, click "Manage"
![img alt](/img/tutorial/twitch-dev-create3.png)

7. Copy the Client ID and the Client Sercret into the Spotch app\
⚠️ Press "New Secret" to make Secret Visible
![img alt](/img/tutorial/twitch-dev-create4.png)
![img alt](/img/tutorial/twitch-dev-create5.png)

8. Click Save and Authenticate in the Spotch App\
A new Tab should open and ask for Permission.\
Once accepted you should see this:\
```{"message":"Access token received and application restarted successfully!"}```

Your Twitch App is now Authenticated!

### Channel Point Rewards

Go to the Rewards section of the Spotch Bot App.
![img alt](/img/tutorial/spotchbot-rewards.png)

At first the Rewards list is empty.
Can add Rewards using the little "+" icon. 

Select a name, description and channel point cost to your liking.
Select the type of the reward. 
There can only be 1 reward of any type. 
![img alt](/img/tutorial/spotchbot-rewards-add.png)

:::info
Make sure to set the Reward to active!

You can always toggle the reward on and off in the list view too!!!
:::
![img alt](/img/tutorial/spotchbot-rewards-list.png)