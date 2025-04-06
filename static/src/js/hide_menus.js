/** @odoo-module **/

import { registry } from "@web/core/registry"; // Importamos el registro de Odoo

// 🔹 Eliminar elementos del menú de usuario
const userMenu = registry.category("user_menuitems");
if (userMenu) {
    const itemsToRemove = [
        "documentation",
        "support",
        "shortcuts",
        "separator",
        "odoo_account",
        "install_pwa",
        "profile"
    ];

    itemsToRemove.forEach(item => userMenu.remove(item));
}

// 🔹 Eliminar el servicio "tour_service"
const services = registry.category("services");
if (services) {
    services.remove("tour_service");
}

// 🔹 Eliminar elementos de la barra superior (systray)
const systray = registry.category("systray");
if (systray) {
    systray.remove("mail.activity_menu");
    systray.remove("mail.messaging_menu");
}

    

