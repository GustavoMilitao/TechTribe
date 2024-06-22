# SPDX-FileCopyrightText: 2023 
#
# SPDX-License-Identifier: MPL-2.0


from fastapi import APIRouter, Depends, HTTPException

from techtribe.auth import get_current_user
from techtribe.db.models import User, GameInLobby
from techtribe.config import redis

router = APIRouter()


@router.get("/game_waiting")
async def get_game_in_lobby(user: User = Depends(get_current_user)):
    game_in_lobby_raw = await redis.get(f"game_in_lobby:{user.id.hex}")
    if game_in_lobby_raw is None:
        raise HTTPException(status_code=404, detail="No game waiting")
    game_in_lobby = GameInLobby.parse_raw(game_in_lobby_raw)
    return game_in_lobby
