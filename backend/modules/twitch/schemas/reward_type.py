import enum

class RewardType(enum.Enum):
    SONG_QUEUE_ADD = ("song_queue_add", "Song Queue Add")
    PLAYLIST_ADD = ("playlist_add", "Playlist Add")

    def __init__(self, technical_label: str, user_label: str):
        self.technical_label = technical_label
        self.user_label = user_label

    @classmethod
    def get_user_labels(cls):
        """Return a list of user-friendly labels."""
        return [reward_type.user_label for reward_type in cls]

    @classmethod
    def get_technical_labels(cls):
        """Return a list of technical labels."""
        return [reward_type.technical_label for reward_type in cls]

    @classmethod
    def get_label_mapping(cls):
        """Return a mapping of technical labels to user-friendly labels."""
        return {reward_type.technical_label: reward_type.user_label for reward_type in cls}
