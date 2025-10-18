import eventlet
eventlet.monkey_patch()
from app import create_tables, app, email


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    debug = os.getenv('DEBUG') == "True"
    create_tables()
    app.run(host="0.0.0.0", port=port, debug=debug)
    