# TgEntities2html

With this library you can parse the entities of a Telegram message to return html.


## Install
`pip install TgEntities2html`


## Use
`import TgEntities2html

json_message = open("telegram_message.json", "r", encoding="utf-8").read()

TgEntities2html.getHtml(json_message)
`
