import flet as ft
from classes import Message
from classes import ChatMessage
        

def main(page: ft.Page):
    #função para envio da mensagem do texfield ao clicar no botão enviar
    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(
                Message(
                    page.session.get("user_name"),
                    new_message.value,
                    message_type="chat_message",
                )
            )
        new_message.value = ""
        new_message.focus()
        page.update()
        
    def join_click(e):
        if not user_name.value:
            user_name.error_text = "Nome não pode ficar em branco!"
            user_name.update()
        else:
            page.session.set("user_name", user_name.value)
            page.dialog.open = False
            page.pubsub.send_all(Message(user_name=user_name.value, text=f"{user_name.value} Entrou no chat.", message_type="login_message"))
            page.update()  

    #função para enviar mensagem para todo mundo da seção
    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.GREY_300, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message) 

    #variaveis
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = "Chat dos Cria"
    page.update()
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )
    new_message = ft.TextField(
        hint_text="Escreva uma mensagem...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )
    user_name = ft.TextField(label="Lança teu Vulgo")

    #Modal para selecionar o nome do usuário
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Salve!"),
        content=ft.Column([user_name], tight=True),
        actions=[ft.ElevatedButton(text="Entra ai irmão", on_click=join_click)],
        actions_alignment="end",
    )

    page.add (
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Manda a mensagem",
                    on_click=send_message_click,
                ),
            ]
        ),
    )

   

ft.app(target=main, view=ft.WEB_BROWSER)