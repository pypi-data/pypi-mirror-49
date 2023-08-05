# WxWork group bot API client
## usage
```
from wxworkbot import Bot
# https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}
bot = Bot(bot_name='test', key='YOUR_KEY_HERE') 
bot.send_text_mentioned('BIG NEWS!', mentioned_list=['all'])
```
> see more on [official document](https://work.weixin.qq.com/api/doc?notreplace=true#90000/90135/91760)
