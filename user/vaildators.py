from .models import User

def vaildate_user_data(user_data):
    username = user_data.get("username")
    nickname = user_data.get("nickname")
    password = user_data.get("password")

    err_message = []

    if len(nickname) > 15:
        err_message.append("닉네임은 15글자 이하로 작성해주세요.")

    if len(password) < 8:
        err_message.append("비밀번호는 최소 8글자여야 합니다.")
    
    if User.objects.filter(username=username).exists():
        err_message.append("이미 존재하는 아이디입니다.")    
    
    if err_message:
        return err_message
    return None