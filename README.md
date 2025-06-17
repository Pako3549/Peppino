<div align="center">

![](https://cdn.discordapp.com/app-icons/1384568070072172714/d8c81fd0f89d09d4d83c940c2f3c2d11.png?size=512)

# Peppino A/D ⚔️🛡️
![](https://img.shields.io/github/last-commit/Pako3549/Peppino?&style=for-the-badge&color=8272a4&logoColor=D9E0EE&labelColor=292324)
![](https://img.shields.io/github/stars/Pako3549/Peppino?style=for-the-badge&logo=polestar&color=FFB1C8&logoColor=D9E0EE&labelColor=292324)
![](https://img.shields.io/github/repo-size/Pako3549/Peppino?color=CAC992&label=SIZE&logo=files&style=for-the-badge&logoColor=D9E0EE&labelColor=292324)

</div>

**Peppino** is a Discord bot written in Python designed to monitor service availability during Attack/Defense (A/D) style CTF competitions. The bot continuously checks if the services are up or down and sends alerts to a specified Discord channel.

## 🛠️ Main Features

- **Service Monitoring**: Continuously check the status of configured services.
- **Real-time Alerts**: Notify a specific Discord channel if services go down or come back online.
- **News Channel**: Choose the Discord channel where alerts are posted by setting the channel ID in the source code.
- **Asynchronous Checks**: Uses aiohttp for efficient, non-blocking HTTP requests.
- **Multi-Service Support**: Monitor multiple services simultaneously.

## 📋 Prerequisites

Before running the bot, make sure you have:
- Python 3.8 or higher installed.
- A Discord bot token (obtainable from the Discord Developer Portal).
- The following Python libraries installed:
  - `discord.py`
  - `python-dotenv`
  - `aiohttp`

## ⚙️ Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Pako3549/Peppino.git
    ```
2. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Configure the `.env` file**: Create a `.env` file in the main directory and add your bot token, api url and discord channel id:
    ```env
    token=YOUR_BOT_TOKEN
    API_URL=YOUR_API_URL
    NEWS_CHANNEL_ID=YOUR_NEWS_CHANNEL_ID
    ```
1. **Run the bot**:
    ```bash
    python main.py
    ```

## 📖 How to Use

- The bot will automatically start monitoring the configured services.
- When a service goes down, it sends an alert message in the chosen Discord channel.
- When the service is back online, it sends a recovery notification.
- The monitoring runs continuously until the bot is stopped.

## 🐛 Troubleshooting

- **Bot not sending messages?**
  
  Check that the bot has permission to send messages in the configured Discord channel.

- **Services not detected correctly?**
  
  Verify that the service URLs or IPs in the source code are correct and reachable.

- **Bot crashes or errors?**
  
  Check the console logs for error details.

## 📜 License

This project is open-source and available under the GPL-3.0 License. See the [LICENSE](https://github.com/Pako3549/Peppino/blob/main/LICENSE) file for more details.
