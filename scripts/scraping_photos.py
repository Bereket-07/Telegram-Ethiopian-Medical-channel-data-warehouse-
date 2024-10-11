from telethon import TelegramClient
import csv , os , logging , json
from dotenv import load_dotenv

# set upt logging
logging.basicConfig(
    filename='../photoscraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment Variables once
load_dotenv()
api_id = int(os.getenv('TG_API_ID'))
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Functions to read channels from  JSON file
def load_channels_from_json(file_path):
    try:
        with open(file_path,'r') as f:
            data = json.load(f)
            return data.get('channels',[]),data.get('comments' , [])
    except Exception as e:
        logging.error(f"error reading channels from JSON: {e}")
        return [],[]
# funciton to scrape data from a single channel
async def scrape_channel(clinet,channel_username,writer,media_dir,num_messages):
    try:
        entity = await clinet.get_entity(channel_username)
        channel_title = entity.title
        message_count = 0
        async for message in client.iter_messages(entity , limit=1000):
            if message_count >= num_messages:
                break # stop after scraping the specific number ofmessages
            media_path = None
            if message.media:
                filename = f"{channel_username}_{message.id}.{message.media.document.mime_type.split('/')[-1]}"if hasattr(message.media, 'document') else f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir,filename)
                await client.download_media(message.media,media_path)
                logging.info(f"Download media for messge ID {message.id}")
            writer.writerow([channel_title, channel_username , message.id ,  message.date , media_path])
            logging.info(f"Processed message ID {message.id} from{channel_username}")
            message_count += 1
            if message_count == 0:
                logging.info(f"No message found for {channel_username}")
    except Exception as e:
        logging.error(f"error ocured while scraping data from the channel: {e}")
#  Initialize the client once with a session file
client = TelegramClient('scraping_session',api_id,api_hash)

async def main(telegram_channel_username_path):
    try:
        await client.start(phone)
        logging.info("Client Started successfully.")
        media_dir = '../photos/YOLO'
        os.makedirs(media_dir,exist_ok=True)

        # Load channels from JSON file
        channels , comments = load_channels_from_json(telegram_channel_username_path)

        num_messages_to_scrape = 2000  # specify the number of messages to scrape
        for channel in channels:
            # Create a CSV file named after the channel
            csv_filename = f"../data/YOLO/{channel[1:]}_data.csv" # i removed '@' from the data set name
            with open(csv_filename,'a',newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Channel Title' ,'Channel Username' , 'ID' , 'Media Path'])
                await scrape_channel(client,channel,writer,media_dir,num_messages_to_scrape)
                logging.info(f"Scraped data from {channel}.")
            # log commented channels if needed 
            if comments:
                logging.info(f"Commented channels: {','.join(comments)}")
    except Exception as e:
        logging.error(f"error in main function: {e}")
        

if __name__ == '__main__':
    import asyncio
    asyncio.run(main('../tg_channels/YOLOchannels.json'))