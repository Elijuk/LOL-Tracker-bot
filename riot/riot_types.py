# ========== Imports ==========
from typing import TypedDict, Any


# ========== TypeDicts ==========
class BanData(TypedDict):
    championId: int
    pickTurn: int

class ObjectiveData(TypedDict):
    first: bool
    kills: int

class ObjectivesData(TypedDict):
    baron: ObjectiveData
    dragon: ObjectiveData
    tower: ObjectiveData
    riftHerald: ObjectiveData
    inhibitor: ObjectiveData

class TeamData(TypedDict):
    teamId: int
    win: bool
    bans: list[BanData]
    objectives: ObjectivesData

class GameInfo(TypedDict):
    gameStartTimestamp: int
    gameDuration: int
    gameMode: str
    teams: list[TeamData]

class MatchMetadata(TypedDict):
    matchId: str
    participants: list[str]

class ParticipantData(TypedDict, total=False):
    puuid: str
    championName: str

class MatchData(TypedDict):
    metadata: MatchMetadata
    info: GameInfo
