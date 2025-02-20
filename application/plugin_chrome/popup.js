document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("qrcode-form");

    if (form) {
        form.addEventListener("submit", async function(event) {
            event.preventDefault();

            let valor = parseFloat(document.getElementById("valor").value);
            const chave = document.getElementById("chave").value;
            let calendario = document.getElementById('calendario').value;
            const cpf = document.getElementById('devedor_cpf').value;
            const nome = document.getElementById('devedor_nome').value;

            calendario = parseInt(calendario, 10);

            if (isNaN(calendario)) {
                alert("O valor de expiração deve ser um número válido.");
                return;
            }

            if (!isNaN(valor)) {
                valor = valor.toFixed(2);
            } else {
                alert("O valor inserido não é um número válido.");
                return;
            }

            const data = {
                valor: { original: valor },
                chave: chave,
                calendario: { expiracao: calendario },
                devedor: { cpf: cpf, nome: nome },
                solicitacaoPagador: document.getElementById('solicitacaoPagador').value
            };

            try {
                const response = await fetch("https://efi.comnect.com.br/cob_imediata_plugin", {  // Chama o endpoint correto do Flask
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                console.log("Resultado da resposta do servidor:", result);

                if (response.ok) {
                    document.getElementById("result").innerHTML = `
                        <h3>QR Code Gerado:</h3>
                        <p><b>PIX Copia e Cola:</b> ${result.pixCopiaECola}</p>
                        <p><b>Link de Visualização:</b> <a href="${result.linkVisualizacao}" target="_blank">${result.linkVisualizacao}</a></p>
                        <img src="${result.qrcodeImagem}" alt="QRCode"/>
                    `;
                } else {
                    document.getElementById("result").innerHTML = `
                        <h3>Erro:</h3>
                        <p>${result.error || 'Erro desconhecido'}</p>
                    `;
                }
            } catch (error) {
                console.error("Erro ao se comunicar com o servidor:", error);
                document.getElementById("result").innerHTML = `
                    <h3>Erro:</h3>
                    <p>Erro ao se comunicar com o servidor.</p>
                `;
            }
        });
    } else {
        console.error("Formulário não encontrado!");
    }
});