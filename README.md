# toersten-discord-bot

Toersten daily task is to drink beer and handle the people in Ödets discord! 

## Instructions

When doing development run the command in the main folder to start the server:

```python

python bot.py ["ID of bot, e.g. 0001"] ["password"]
```

To be able to run the bot locally you need the following moduals:

- pyppeteer==0.0.18
- discord#rewrite
- gpiozero
All modules are installed via pip, but since the discor#rewrite isn't hosted on official repositorys you have to use this command instead: 

```python
pip install -U git+https://github.com/Rapptz/discord.py@rewrite
```

## Current Features

- Check latency
- Check version
- React on certian comments
- Get course information from Ladok
- Bug report with notification to admins
- Locals bots for development and hosted bot for service
- Encryted bot IDs

## Todo

- Automatically set user privileges according to their course attendance on Blackboard
- Create Youtube-playlist with Nolle-listan
- Update courses which has no courseID yet

## Commands

| Command       | Description                                   |
|---------------|-----------------------------------------------|
| 7: ping       | Check latency                                 |
| 7: version    | Check bot version                             |
| 7: courses    | Returns course attendance from Blackboard     |
| 7: report     | To report a bug or issue to admins            |
| 7: register   | To get courseID from Blackboard               |
| 7: help       | Returns commands to write                     |
| 7: todo       | Returns the todo-list (admins only)           |
| 7: add        | Adds a string to the todo-list (admin only)   |

## Contributors

- [Martin Myhrman](https://github.com/myhrmans/)
- [Karl-Johan Djervbrant](https://github.com/kallekj/)
- [Andreas Häggström](https://github.com/AndreasH96/)
- [Filip Göranson](https://github.com/filipgoranson/)