class Tienda {
  constructor() {
    this.attachEvents()
  }

  attachEvents() {
    /**
     * Wrap django errolist and helptext
     */
    $('.errorlist').addClass('alert alert-danger')
    $('.helptext').wrapAll("<div class='alert alert-info'></div>")
    /**
     * Attach key event for busqueda field
     */
    let _this = this;
    $('input#busqueda').keydown(function (e) {
      if (e.keyCode === 13) {
        _this.busca()
      }
    })
  }

  busca() {
    this.textoBusqueda = $('input#busqueda').val().toLowerCase();
    if (this.textoBusqueda.length >= 3) {
      window.location = '/busqueda/' + this.textoBusqueda + '/'
    } else {
      $('div#val-busqueda').removeClass('hide')
    }
  }
}

let tienda = new Tienda()

class Carro {
  constructor() {
    this.actualizando = false;
  }

  actualiza = (path) => {
    if (!this.actualizando) {
      this.actualizando = true;
      $.ajax({
        url: path,
        success: (result) => $("#carrito-ajax").html(result),
        complete: () => this.actualizando = false
      })
    }
  }
}

const carro = new Carro();
