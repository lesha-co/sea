from clients import ConsoleClient, BotClient
from config import Response, Theme, Locale


class Server:

    def __init__(self) -> None:
        locale = Locale.RU
        player_a = ConsoleClient(locale, Theme.MAIN, border=True, client_id='Кожаный мешок')
        player_b = BotClient(client_id='Робот', locale=locale)

        current_player = player_a
        target_player = player_b

        while True:
            # Запрашиваем у текущего игрока ход:
            move = current_player.request_move(
                target_player.field.get_view(opponent=True)
            )

            # стреляем в поле противника
            response = target_player.field.hit(move)

            # показываем игроку ответ
            current_player.message(str(response.value))

            # обновляем состояние игры
            if response == Response.MISS:
                # меняем игроков местами
                current_player, target_player = target_player, current_player
            if response == Response.LOST:
                # оповещаем игроков о конце игры
                current_player.conclude('Вы выиграли!', target_player.field.get_view())
                target_player.conclude('Вы проиграли!', current_player.field.get_view())
                break


if __name__ == '__main__':
    Server()
