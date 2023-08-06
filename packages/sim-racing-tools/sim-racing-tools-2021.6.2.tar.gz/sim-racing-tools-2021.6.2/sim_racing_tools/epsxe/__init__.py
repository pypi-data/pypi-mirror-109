from steam.steamid import SteamID


def install_epsxe():
    pass


def add_game_to_steam(steam_id=None, steam_account_number=None):
    if not steam_id and not steam_account_number:
        raise ValueError("Must provide steam_id or steam_partner_id")

    if steam_id:
        folder_name = str(SteamID(steam_id) & 0xFFFFFFFE)
    else:
        folder_name = str(steam_account_number)


