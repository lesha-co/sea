from clients import ConsoleClient, BotClient
from config import Response, Theme, Locale


class Server:

    def __init__(self) -> None:
        player_a = ConsoleClient(Locale.RU, Theme.MAIN, border=True, client_id='Кожаный мешок')
        player_b = BotClient(client_id='Робот')

        current_player = player_a
        target_player = player_b

        while True:
            # Запрашиваем у текущего игрока ход:
            move = current_player.request_move(
                current_player.field,
                # это раскрывает поле игрока для противника, но мы честные люди и
                # будем использовать его только для отрисовки в режиме оппонента:
                target_player.field
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
                current_player.message('Вы выиграли!')
                target_player.message('Вы проиграли!')
                break


if __name__ == '__main__':
    Server()
