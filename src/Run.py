from src import config, create_app

app = create_app(config.Config)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
