{
    "name": "ThingsBoard REST API For Odoo",
    "version": "1.0",
    "category": "API",
    "author": "Feitas",
    "website": "",
    "summary": "ThingsBoard REST API For Odoo16",
    "support": "",
    "description": """
ThingsBoard REST API For Odoo
=============================
""",
    "depends": ["web", "maintenance", "project", "fleet"],
    "data": [
        'views/res_config_settings_view.xml',
        'views/maintenance_views_ext.xml',
        'views/project_views_ext.xml',
        'views/project_task_views_ext.xml',
        'views/fleet_vehicle_views_ext.xml',
    ],
    "external_dependencies": {
        "python": ["tb-rest-client"]
    },
    "images": [],
    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
}
