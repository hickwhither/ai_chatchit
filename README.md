# AI chat chit

A cool AI a made with ollama
Một bot AI chat xịn xò vjp xjljp

## 2024w24.10 (Open test)
- First commit
- AI no longer responds to every message, but only sends messages every ~10-20 seconds like a human.

Vietnamese ver:
- AI không còn trả lời tất cả tin nhắn, nhưng chỉ gửi tin nhắn sau mỗi ~ 10-20 giây như một người.
`
## Installation and usage
Script side:
- Required: Python 3.12.x
- Install all libraries in `requirements.txt`

Ollama side:
- Install Ollama
- Download any model you want

Put your bot credentials in `.env` file:
```env
APPLICATION_ID = your_app_id
TOKEN = your_bot_token
```
Set `MODEL` variable in `cogs/aipromt.py` with the model you want to use

Run the bot:
```sh
python main.py
```

## Installation and usage (Vietnamese)
Phía script:
- Yêu cầu: Python 3.12.x
- Cài đặt tất cả thư viện trong `requirements.txt`

Phía Ollama:
- Cài đặt Ollama
- Tải bất kỳ model nào bạn muốn

Đặt thông tin bot của bạn vào file `.env`:
```
APPLICATION_ID = your_app_id
TOKEN = your_bot_token
```
Đặt biến `MODEL` trong `cogs/aipromt.py` với model bạn muốn sử dụng

Chạy bot:
```
python main.py
```
