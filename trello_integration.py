from trello import TrelloClient
import app_config
client = TrelloClient(
    api_key=app_config.API_KEY,
    api_secret=app_config.API_SECRET,
    token=app_config.TOKEN
)

client.add_board('test2')