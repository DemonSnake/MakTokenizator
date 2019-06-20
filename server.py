"""
Module for web query server
"""
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    """
    Class for managing events
    """

    def do_GET(self):
        """
        Method which runs when webpage is opened
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        htmlc = """
                <html>
                    <body>
                        <form method=”post”>
                            <input type = “text” name = “query”>
                            <input type = “submit”>
                        </form>
                    </body>
                </html>
                """
        self.wfile.write(bytes(htmlc, encoding="UTF-8"))


if __name__ == "__main__":
    server = HTTPServer(('', 80), RequestHandler)
    server.serve_forever()