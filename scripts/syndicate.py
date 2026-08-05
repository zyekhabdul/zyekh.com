import os
import sys
import subprocess
import xml.etree.ElementTree as ET
import urllib.request
import json

def get_new_feed_items():
    try:
        current_feed = subprocess.check_output(['git', 'show', 'HEAD:feed.xml']).decode('utf-8')
        prev_feed = subprocess.check_output(['git', 'show', 'HEAD~1:feed.xml']).decode('utf-8')
    except Exception as e:
        print("Could not retrieve git history for feed.xml. This might be the first commit or an error occurred.")
        return []

    try:
        curr_root = ET.fromstring(current_feed)
        prev_root = ET.fromstring(prev_feed)
    except ET.ParseError:
        print("Failed to parse XML.")
        return []

    curr_items = {item.find('link').text: item for item in curr_root.findall('.//item') if item.find('link') is not None}
    prev_links = {item.find('link').text for item in prev_root.findall('.//item') if item.find('link') is not None}

    new_items = []
    for link, item in curr_items.items():
        if link not in prev_links:
            title_node = item.find('title')
            desc_node = item.find('description')
            new_items.append({
                'title': title_node.text if title_node is not None else 'No Title',
                'link': link,
                'description': desc_node.text if desc_node is not None else ''
            })
    return new_items

def notify_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps({'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
        print("Telegram notification sent.")
    except Exception as e:
        print(f"Telegram failed: {e}")

def notify_discord(webhook_url, content):
    data = json.dumps({'content': content}).encode('utf-8')
    req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    try:
        urllib.request.urlopen(req)
        print("Discord notification sent.")
    except Exception as e:
        print(f"Discord failed: {e}")

def main():
    new_items = get_new_feed_items()
    if not new_items:
        print("No new RSS items found. Exiting.")
        sys.exit(0)

    telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    telegram_chat = os.environ.get('TELEGRAM_CHAT_ID')
    discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')

    for item in new_items:
        msg = f"[ UPDATE ] New Architecture Blueprint Published!\n\n**{item['title']}**\n{item['description']}\n\n[Read Full Article ->]({item['link']})"
        
        if telegram_token and telegram_chat:
            notify_telegram(telegram_token, telegram_chat, msg)
        
        if discord_webhook:
            notify_discord(discord_webhook, msg)

if __name__ == "__main__":
    main()
