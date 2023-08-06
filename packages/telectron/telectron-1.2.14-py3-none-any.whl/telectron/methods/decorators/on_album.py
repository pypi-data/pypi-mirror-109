from threading import Lock
import asyncio
from telectron import filters
from telectron.scaffold import Scaffold

album_messages_filter = filters.create(lambda _, __, m: m.media_group_id)

ALBUM_HACK_DELAY = 1


class OnAlbum(Scaffold):
    def on_album(self, *args, **kwargs):
        self.albums = TAlbums(self)
        return self.albums.on_album_messages(*args, **kwargs)


class TAlbums:
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client
        self.albums = {}
        self.lock = Lock()

    def add_album(self, media_group_id, handler):
        self.albums[media_group_id] = Album(self.telegram_client, media_group_id, self.dispatch_event, handler)

    def get_album(self, media_group_id):
        return self.albums.get(media_group_id)

    def dispatch_event(self, media_group_id):
        with self.lock:
            album = self.albums[media_group_id]
            album.handler(self.telegram_client, album.messages)
            del self.albums[media_group_id]

    def on_album_messages(self, messages_filters=None, **kwargs):
        on_message_filters = (album_messages_filter & messages_filters
                              if messages_filters
                              else album_messages_filter)

        def decorator(function):

            @self.telegram_client.on_message(on_message_filters, **kwargs)
            def on_message(client, message):
                with self.lock:
                    album = self.get_album(message.media_group_id)
                    if not album:
                        self.add_album(message.media_group_id, function)
                        album = self.get_album(message.media_group_id)
                with album.lock:
                    album.add_message(message)

            self.last_handler = on_message
            return function
        return decorator


class Album:
    def __init__(self, telegram_client, media_group_id, dispatch_event, handler):
        self.telegram_client = telegram_client
        self.media_group_id = media_group_id
        self.dispatch_event = dispatch_event
        self.handler = handler
        self.lock = Lock()
        self.messages = []
        self.due = self.telegram_client.loop.time() + ALBUM_HACK_DELAY

        telegram_client.loop.create_task(self.deliver_event())

    def add_message(self, message):
        self.messages.append(message)

        self.due = self.telegram_client.loop.time() + ALBUM_HACK_DELAY

    async def deliver_event(self):
        while True:
            diff = self.due - self.telegram_client.loop.time()
            if diff <= 0:
                self.telegram_client.loop.run_in_executor(None, self.dispatch_event, self.media_group_id)
                return

            await asyncio.sleep(diff)
