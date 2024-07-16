# Telegram Jira Bot

This is a Telegram bot that creates issues in cloud Jira and provides two-way communication through chat. It is mostly based on [MasterGroosha's telegram-feedback-bot](https://github.com/MasterGroosha/telegram-feedback-bot).

## Requirements

To use this bot, you need to provide the following:

1. **Issue Key**: Also called "project key", it depends on the name of a project and looks like an uppercase word (e.g., `TEST`).
2. **Jira Instance URL**: The URL of your Jira instance (e.g., `https://yourinstance.atlassian.net/`).
3. **Jira API Token**: You can create one [here](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/).
4. **Jira User ID**: Find your account ID [here](https://community.atlassian.com/t5/Jira-questions/where-can-i-find-my-Account-ID/qaq-p/976527).
5. **Email**: The email of the Jira user.
6. **Telegram API Token**: Obtain one from [BotFather](https://telegram.me/BotFather).
7. **Redis DSN**: Defaults to `redis://default:admin@redis:6379`.
8. **Chat ID**: The ID of the chat where the bot will send messages (use [myidbot](https://telegram.me/myidbot) to find it).

## Configuration

This bot uses custom fields which can be found in `settings.toml`. In Jira, custom fields can be changed only by their IDs. If you plan to use this bot in an existing Jira project, you may need to change the IDs in the following files:
- `jira_bot/jira_manager.py`
- `jira_bot/handlers/ticket.py`

Replace `customfield_10032` and similar fields to match your custom field IDs.

## Usage

To start the bot, use the following command:

```bash
docker-compose up -d
```