/* Oculta o menu lateral padrão do Django Admin */
.nav-sidebar {
    display: none !important; /* Usa !important para garantir que o estilo seja aplicado */
}

/* Ajusta o espaço para o conteúdo principal */
#content-main {
    margin-left: 0 !important; /* Remove a margem esquerda */
}

document.addEventListener('DOMContentLoaded', function() {
    // Lógica para o botão de alternância do menu lateral
    var toggleNavButton = document.querySelector('.nav-toggler');
    var sideNav = document.querySelector('#nav-sidebar');

    if (toggleNavButton && sideNav) {
        sideNav.classList.add('collapsed');

        toggleNavButton.addEventListener('click', function() {
            sideNav.classList.toggle('collapsed');
        });

        // Recolher o menu lateral quando uma opção do menu superior for clicada
        var topMenuLinks = document.querySelectorAll('.custom-admin-menu a');
        topMenuLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                sideNav.classList.add('collapsed');
            });
        });
    }

    // Adiciona lógica para exibir o submenu ao passar o mouse
    var menuItems = document.querySelectorAll('#menu .custom-admin-menu > li');

    menuItems.forEach(function(item) {
        var submenu = item.querySelector('.dropdown-menu');
        if (submenu) {
            item.addEventListener('mouseover', function() {
                submenu.style.display = 'block';
            });

            item.addEventListener('mouseout', function() {
                submenu.style.display = 'none';
            });
        }
    });

    // Fecha o submenu quando clicado fora
    document.addEventListener('DOMContentLoaded', function() {
    var menuItems = document.querySelectorAll('.custom-admin-menu li');
    menuItems.forEach(function(item) {
        item.addEventListener('mouseenter', function() {
            var dropdown = item.querySelector('.dropdown-menu');
            if (dropdown) {
                dropdown.style.display = 'block';
            }
        });

        item.addEventListener('mouseleave', function() {
            var dropdown = item.querySelector('.dropdown-menu');
            if (dropdown) {
                setTimeout(function() {
                    dropdown.style.display = 'none';
                }, 500); // Retarda o desaparecimento por 500ms
            }
        });
    });
});

