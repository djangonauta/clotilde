function configurarAutomacoes() {
  document.querySelectorAll('[automacao]').forEach(function (element) {
    const SUCESSO = 2;
    const ERRO = 3;

    var id_processo;
    var poolling;

    const botaoIniciar = element.querySelector('.iniciar');
    const botaoPausar = element.querySelector('.pausar');
    const botaoContinuar = element.querySelector('.continuar');
    const botaoCancelar = element.querySelector('.cancelar');

    function iniciar() {
      botaoIniciar.disabled = false;
      botaoPausar.disabled = true;
      botaoContinuar.disabled = true;
      botaoCancelar.disabled = true;
    }

    iniciar();

    function iniciarAtivo() {
      botaoIniciar.disabled = true;
      botaoPausar.disabled = false;
      botaoContinuar.disabled = true;
      botaoCancelar.disabled = false;
    }

    function pausarAtivo() {
      botaoIniciar.disabled = true;
      botaoPausar.disabled = true;
      botaoContinuar.disabled = false;
      botaoCancelar.disabled = false;
    }

    function continuarAtivo() {
      botaoIniciar.disabled = true;
      botaoPausar.disabled = false;
      botaoContinuar.disabled = true;
      botaoCancelar.disabled = false;
    }


    botaoIniciar.addEventListener('click', async function () {
      if (!confirm('Deseja iniciar essa automação?')) {
        return
      }
      iniciarAtivo();

      const barraProgresso = element.querySelector('.progress-bar');
      barraProgresso.style = `width: 0%`

      const url = element.dataset.url;
      try {
        const response = await fetch(url, {});
        if (!response.ok) {
          throw new Error(`Erro HTTP: ${response.status} - ${response.statusText}`);
        }
        const data = await response.json();
        console.log(data);
        const id_automacao = data.id_automacao;
        id_processo = data.id_processo;

        poolling = setInterval(verificar, 200);
        async function verificar() {
          try {
            const response = await fetch('/automacoes/verificar/' + id_automacao + '/', {});
            if (!response.ok) {
              throw new Error(`Erro HTTP: ${response.status} - ${response.statusText}`);
            }
            const data = await response.json();
            barraProgresso.style = `width: ${data.porcentagem}%`
            if (data.porcentagem >= 100 || data.status === SUCESSO || data.status === ERRO) {
              iniciar();
              clearInterval(poolling);
              if (data.status === ERRO) {
                console.log(data);
                alert('Erro ao executar automação: \n' + data.stack_trace);
              }
            }
          } catch (error) {
            clearInterval(poolling);
            iniciar();
            console.log(error);
            alert('Erro ao tentar verificar a automação: ' + error.message);
          }
        }

      } catch (error) {
        clearInterval(poolling);
        iniciar();
        console.log(error);
        alert('Erro ao tentar iniciar a automação: ' + error.message);
      }
    });

    botaoPausar.addEventListener('click', async function () {
      if (!confirm('Deseja pausar essa automação?')) {
        return
      }
      pausarAtivo();
      var url = '/automacoes/pausar/' + id_processo + '/';
      try {
        const response = await fetch(url, {});
        const data = await response.json()
        console.log(data);

      } catch (error) {
        clearInterval(poolling);
        iniciar();
        console.log(error);
        alert('Erro ao tentar pausar a automação: ' + error.message);
      }
    });

    botaoContinuar.addEventListener('click', async function () {
      if (!confirm('Deseja continuar essa automação?')) {
        return
      }
      var url = '/automacoes/continuar/' + id_processo + '/';
      try {
        const response = await fetch(url, {});
        const data = await response.json()
        console.log(data)
        continuarAtivo();

      } catch (error) {
        clearInterval(poolling);
        iniciar();
        console.log(error);
        alert('Erro ao tentar continuar a automação: ' + error.message);
      }
    });

    botaoCancelar.addEventListener('click', async function() {
      if (!confirm('Deseja cancelar essa automação?')) {
        return
      }
      try {
        const response = await fetch('/automacoes/cancelar/' + id_processo + '/', {});
        if (!response.ok) {
          throw new Error(`Erro HTTP: ${response.status} - ${response.statusText}`);
        }
        const data = await response.json();
        console.log(data)
        clearInterval(poolling);
        iniciar();

      } catch (error) {
        clearInterval(poolling);
        iniciar();
        console.log(error);
        alert('Erro ao tentar cancelar a automação: ' + error.message);
      }
    })
  });
}

$(function () {
  setTimeout(function () {
    $('[primeiro-campo]').focus();
  }, 300);

  configurarAutomacoes();
});
