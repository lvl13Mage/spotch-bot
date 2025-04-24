import enum

class RewardType(str, enum.Enum):
    SONG_QUEUE_ADD = "song_queue_add"
    PLAYLIST_ADD = "playlist_add"
