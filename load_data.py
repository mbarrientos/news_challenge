import json
import os

from news.models import Channel, Audience

def init_channels():
    for c in CHANNELS:
        Channel(name=c).save()

init_channels()

with open(os.path.join(FILES_DIR, AUDIENCE_FILE)) as f:
    audience = json.load(f)

    for epoch, sizes in audience.items():
        for idx, s in enumerate(sizes):
            Audience(channel=CHANNELS[idx], value=sizes[idx], timestamp=epoch).save()


