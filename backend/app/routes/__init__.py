"""
AgroGuard Backend - Routes Package

Registers all API route blueprints.
"""

def register_blueprints(app):
    from app.routes.auth_routes import auth_bp
    from app.routes.scan_routes import scan_bp
    from app.routes.report_routes import report_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(scan_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(admin_bp)
