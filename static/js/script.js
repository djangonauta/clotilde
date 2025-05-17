// static/js/script.js
console.log("Script carregado com sucesso!");

// Adiciona um evento quando o documento estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log("Documento carregado!");
    
    // Adiciona um texto para confirmar que o JS está funcionando
    const staticTest = document.querySelector('.static-test');
    if (staticTest) {
        const jsConfirm = document.createElement('p');
        jsConfirm.textContent = 'JavaScript carregado com sucesso!';
        jsConfirm.style.color = 'green';
        staticTest.appendChild(jsConfirm);
    }
});
