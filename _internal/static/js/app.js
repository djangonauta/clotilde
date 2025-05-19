function configurarAutomacoes() {
  /**
   * Exemplo de botão/âncora:
      <button automatizacao data-url="{% url 'automacoes:automacao_teste' %}" data-mensagem="#mensagem"
          class="automation-button btn-primary-circle pulse-primary">
        <i class="fa-solid fa-file-lines"></i>
      </button>
      <div id="mensagem" class="alert visually-hidden" role="alert"></div>
    */
  document.querySelectorAll('[automatizacao]').forEach(function (element) {
    element.addEventListener('click', function () {
      if (!confirm('Deseja iniciar essa automação?')) {
        return
      }
      var elemento = this;
      elemento.disabled = true;
      var iconeOriginal = elemento.querySelector('i').className;
      elemento.querySelector('i').className = 'fa-solid fa-spinner fa-spin';
      var elementoMensagem = document.querySelector(elemento.dataset.mensagem);

      var id_automacao = null;
      var pollingInterval = null;
      fetch(elemento.dataset.url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
      }).then(function (response) {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Erro ao conectar');
      }).then(function (data) {
        configurarMensagem(data.mensagem, 'alert-info');
        id_automacao = data.id_automacao;
        pollingInterval = setInterval(verificar, 200);
      }).catch(function (error) {
        configurarMensagem('Erro ao iniciar automação', 'alert-danger');
      });

      function configurarMensagem(innerHTML, tipo) {
        elementoMensagem.classList.remove(
          'alert-primary',
          'alert-secondary',
          'alert-success',
          'alert-danger',
          'alert-warning',
          'alert-info',
          'alert-light',
          'alert-dark',
          'alert-link',
          'alert-dismissible',
          'alert-heading',
          'visually-hidden'
        );
        elementoMensagem.classList.add(tipo);
        elementoMensagem.innerHTML = innerHTML;
      }

      function verificar() {
        fetch('/automacoes/verificar/' + id_automacao + '/', {
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        }).then(function (response) {
          if (response.ok) {
            return response.json();
          }
        }).then(function (data) {
          var status = parseInt(data.status);
          if (status === 2) {
            configurarMensagem('Automação finalizada', 'alert-success');
            desligarPooling();
          }
          if (status === 3) {
            configurarMensagem('Erro ao executar automação</br>' + data.id_automacao, 'alert-danger');
            desligarPooling();
          }
        }).catch(function (error) {
          configurarMensagem('Erro ao executar a automação</br>' + data.id_automacao, 'alert-danger');
          desligarPooling();
        });
      }

      function desligarPooling() {
        clearInterval(pollingInterval);

        elemento.disabled = false;
        elemento.querySelector('i').className = iconeOriginal;
      }
    })
  })
}

$(function () {
  setTimeout(function () {
    $('[primeiro-campo]').focus();
  }, 300);

  configurarAutomacoes();
});
