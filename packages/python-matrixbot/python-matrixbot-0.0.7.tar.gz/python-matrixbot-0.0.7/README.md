# python-matrixbot

A Python module meant to act as a base class for a [Matrix](https://matrix.org) bot.

## Compatibility

Python 3.6+

## Installation

    pip install python-matrixbot

## Usage

The MatrixBot class will connect to the Matrix server, start a listener on each joined
room, and listen for room invites from other users. It also includes helper methods you
can use to extend the functionality. It is built on the
[Matrix Python SDK](https://matrix-org.github.io/matrix-python-sdk/) which can be
directly accessed via `MatrixBot.client`

    from matrixbot import MatrixBot

    # create a new bot
    bot = MatrixBot(
        host="example.com",
        display_name="Example Bot",
        token=access_token,
        user_id="@bot:example.com"
    )
    # run forever
    bot.start()

### Get a list of joined rooms:

    room_ids = bot.rooms.keys()
    room_objects = bot.rooms.values()

### Leave abandoned 1-on-1 rooms

    for room in bot.rooms.values():
        bot.leave_if_empty(room)

### Cache results from external API calls

To prevent abuse of commands that rely on external API calls, MatrixBot includes a
very basic caching mechanism. Wrap all API calls in `MatrixBot.fetch()` to return
cached results and automatically refresh stale data.

    def get_url(url):
      return response.get(url)

    result = bot.fetch(
        "cache_key", lambda: get_url("https://example.com"), timeout=900
    )

By default the module uses an in-memory cache which is lost between restarts. To create
a persistent cache provide the constructor with the path to a sqlite database:

    bot = MatrixBot(
        ...
        cache_db="/path/to/sqlite_database"
    )

### Sub-classing
Create a subclass to extend and override default features

    class MyBot(MatrixBot):
        # override `process_message()` to filter/parse/react to room events:
        def process_message(self, room, event):
            # say hello when a user joins the room
            if event["type"] == "m.room.member":
                if event["content"]["membership"] == "join":
                    self.say(room, "Hello!", mention=event["sender"])

        # override `accept_invite()` to disable auto-join:
        def accept_invite(self, room_id):
            pass

    bot = MyBot(...)

## License

MIT

## Maintainer

Brian Ó <blacksam@gibberfish.org>

Contributions welcome.

## About Gibberfish

Gibberfish, Inc is a volunteer nonprofit that develops free tools to promote online
privacy for activists and regular people alike. If you like this module and decide to
use it in your project, please consider donating $1 to help keep us going. Thanks!

https://gibberfish.org/donate/
