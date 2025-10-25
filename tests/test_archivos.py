@app.route('/test/archivos')
def test_archivos():
    """Verifica conexión TCP con el servicio de archivos"""
    try:
        with socket.create_connection((ARCHIVOS_HOST, ARCHIVOS_PORT), timeout=3):
            return jsonify({
                "status": "ok",
                "service": "archivos_service",
                "message": f"Conexión TCP exitosa a {ARCHIVOS_HOST}:{ARCHIVOS_PORT}"
            }), 200
    except Exception as e:
        logging.error(f"Error conectando con archivos_service: {e}")
        return jsonify({
            "status": "error",
            "service": "archivos_service",
            "message": str(e)
        }), 500
