from app import app, is_debug

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=is_debug)
