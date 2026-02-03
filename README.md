Gestor de Ponto - Filtro por Período (AFD v671)

Este é um aplicativo desktop desenvolvido em Python para gestão de funcionários e processamento de ficheiros AFD (Arquivo de Fonte de Dados). Permite filtrar registos de ponto por período e exportar os resultados consolidados para CSV.

🚀 Funcionalidades

Cadastro de Funcionários: Guarda Nome e CPF numa base de dados local (dados.txt).

Visualizador AFD: Permite abrir e ler o conteúdo bruto de ficheiros de relógio de ponto.

Filtro por Período: Processa ficheiros AFD filtrando por datas específicas.

Exportação CSV: Gera relatórios formatados com as horas de entrada e saída.

🛠️ Pré-requisitos

Antes de começar, é necessário ter o Python 3.x instalado no sistema.

No Windows:

O Python geralmente já inclui a biblioteca gráfica necessária. Caso não tenha o Python, pode descarregá-lo em python.org.

No Linux (Ubuntu/Debian e derivados):

A biblioteca tkinter (utilizada para a interface) pode precisar de ser instalada manualmente:

sudo apt update
sudo apt install python3-tk


🏃 Como Executar o Código Fonte

Se desejar apenas executar o programa sem gerar um executável:

Abra o terminal ou linha de comandos na pasta do projeto.

Execute o comando:

python app.py


(Nota: No Linux, poderá ser necessário usar python3 app.py)

📦 Como Gerar um Executável (.exe ou Binário)

Para transformar este script num ficheiro executável que não dependa do terminal para correr, utilizaremos o PyInstaller.

1. Instalar o PyInstaller

No terminal, execute:

pip install pyinstaller


2. Compilar o Projeto

Para gerar um único ficheiro que oculte a janela da consola ao abrir, utilize o comando abaixo:

No Windows:

pyinstaller --noconsole --onefile --name "GestorPonto" app.py


No Linux:

pyinstaller --onefile --name "GestorPonto" app.py


3. Onde encontrar o ficheiro?

Após o término do processo, será criada uma pasta chamada dist. Dentro dela estará o seu executável:

Windows: GestorPonto.exe

Linux: GestorPonto (binário)

📂 Estrutura de Ficheiros

app.py: Código fonte principal em Python.

dados.txt: Gerado automaticamente para guardar a lista de funcionários.

README.md: Este guia de instruções.

⚠️ Observações Importantes

O ficheiro dados.txt é criado na mesma pasta onde o executável/script estiver. Certifique-se de que tem permissões de escrita na pasta.

O formato do AFD suportado segue o padrão de extração onde a linha de registo de ponto (Tipo 3) inicia na posição 9.

Desenvolvido para gestão simplificada de registos de ponto.