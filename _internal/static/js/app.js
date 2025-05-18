$(function () {
  setTimeout(function () {
    $('[primeiro-campo]').focus();
  }, 300);

  document.querySelector('#automacao-teste').addEventListener('click', function (e) {
    if (!confirm('Deseja iniciar essa automação?', "Clotilde gostaria de saber")) {
      return
    }
    var botao = this;
    var id_automacao = null;
    var pollingInterval = null;
    var iconeOriginal = botao.querySelector('i').className;

    botao.disabled = true;
    botao.querySelector('i').className = 'fa-solid fa-spinner fa-spin';

    fetch(botao.dataset.url, {
      headers: {
          'X-Requested-With': 'XMLHttpRequest'
      }
    }).then(function (response) {
      if (response.ok) {
        return response.json()
      }
    }).then(function (data) {
      var mensagem = document.querySelector('#mensagem');
      mensagem.classList.remove('visually-hidden', 'alert-success');
      mensagem.classList.add('alert-info');
      mensagem.innerHTML = data.mensagem;

      id_automacao = data.id_automacao;
      pollingInterval = setInterval(verificar, 200);
    });

    function verificar() {
      fetch('/automacoes/verificar/' + id_automacao + '/', {

      }).then(function (response) {
        return response.json()
      }).then(function (data) {
        if (data.status.toLowerCase() === 'finalizada') {
          var mensagem = document.querySelector('#mensagem')
          mensagem.classList.remove('alert-info');
          mensagem.classList.add('alert-success');
          mensagem.innerHTML = 'Automação finalizada';
  
          clearInterval(pollingInterval);
          botao.disabled = false;
          botao.querySelector('i').className = iconeOriginal;
        }
      })
    }
  })
});
