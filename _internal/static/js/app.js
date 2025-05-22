function configurarAutomacoes() {
  document.querySelectorAll('[automacao]').forEach(function (element) {
    var id_processo;
    var poolling;

    const botaoIniciar = element.querySelector('.iniciar');
    const botaoCancelar = element.querySelector('.cancelar');

    function iniciarAtivo() {
      botaoIniciar.disabled = false;
      botaoCancelar.disabled = true;
    }

    function cancelarAtivo() {
      botaoIniciar.disabled = true;
      botaoCancelar.disabled = false;
    }

    botaoIniciar.addEventListener('click', async function () {
      if (!confirm('Deseja iniciar essa automação?')) {
        return
      }
      cancelarAtivo();

      const barraProgresso = element.querySelector('.progress-bar');
      barraProgresso.style = `width: 0%`

      const response = await fetch('/automacoes/iniciar/', {
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      const data = await response.json();
      const id_automacao = data.id_automacao;
      id_processo = data.id_processo;

      poolling = setInterval(verificar, 200);
      async function verificar() {
        const response = await fetch('/automacoes/verificar/' + id_automacao + '/', {
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        });
        const data = await response.json();
        barraProgresso.style = `width: ${data.porcentagem}%`
        if (data.porcentagem >= 100) {
          iniciarAtivo();
          clearInterval(poolling);
        }
      }
    })

    botaoCancelar.addEventListener('click', async function() {
      if (!confirm('Deseja cancelar essa automação?')) {
        return
      }
      const response = await fetch('/automacoes/cancelar/' + id_processo + '/', {
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      const data = await response.json();
      clearInterval(poolling);
      iniciarAtivo();
    })
  });
}

$(function () {
  setTimeout(function () {
    $('[primeiro-campo]').focus();
  }, 300);

  configurarAutomacoes();
});
