# reddit-aloite_bot

Reddit bot

Kansalaisaloite
* https://www.kansalaisaloite.fi/fi
* https://www.kansalaisaloite.fi/api/

Kuntalaisaloite
* https://www.kuntalaisaloite.fi/fi
* https://www.kuntalaisaloite.fi/api/

## Install
 
* Rename `auth.json.dist` to `auth.json` and add credentials
* Rename `aloite_bot.service.dist` to `aloite_bot.service` and modify directory
* Rename `aloite_bot.timer.dist` to `aloite_bot.timer` and modify service if necessary

Systemd:

    systemctl --user enable $(pwd)/aloite_bot.service
    systemctl --user enable $(pwd)/aloite_bot.timer
    systemctl --user start aloite_bot.timer
    systemctl --user list-units
    systemctl --user list-timers
