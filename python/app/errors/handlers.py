from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found", "dettagli": str(error)}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal server error", "dettagli": str(error)}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        return jsonify({
            "error": "An unexpected error has occurred",
            "details": str(error)
        }), 500
