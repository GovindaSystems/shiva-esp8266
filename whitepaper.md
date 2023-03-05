# Protocolo Shiva-esp8266 Blockchain whitepaper 

O Protocolo Shiva-esp8266 Blockchain é um novo protocolo de blockchain que visa revolucionar a forma como a telemetria de estufas é realizada. Inspirado nos modelos de negócios do Arduino e Tuya, o protocolo Shiva-esp8266 combina o poder da blockchain com dispositivos IoT para fornecer uma solução completa e segura para monitorar e controlar as condições de uma estufa.

## Resumo

## **Dispositivos IoT**
O Protocolo Shiva-esp8266 Blockchain utiliza dispositivos IoT para coletar e transmitir dados de telemetria. O protocolo fornece orientações detalhadas sobre como programar o Micro controlador ESP8266 e como realizar autenticação segura para proteger os dados. Além disso, o protocolo também orienta como registrar o dispositivo na AWS IOT, Tuya e Web3, permitindo a integração com outras plataformas de gerenciamento de dispositivos IoT.

## **Blockchain**
O Protocolo Shiva-esp8266 Blockchain utiliza a tecnologia blockchain para garantir a segurança e a integridade dos dados coletados pelos dispositivos IoT. Os dados são criptografados e armazenados de forma descentralizada na blockchain, impedindo a adulteração ou o acesso não autorizado aos dados.

## **Token Shiva**
O Protocolo Shiva-esp8266 Blockchain também inclui o Token Shiva, que é usado para incentivar os usuários a contribuir com a rede e manter a integridade dos dados. Os usuários que contribuem com a rede recebem tokens como recompensa, que podem ser usados para acessar recursos adicionais ou trocados por outras criptomoedas em exchanges.

## **Modelo de negócio do Arduino**
O Protocolo Shiva-esp8266 Blockchain segue o modelo de negócio do Arduino, permitindo que os usuários criem seus próprios dispositivos IoT personalizados usando o Micro controlador ESP8266. O protocolo fornece orientações detalhadas sobre como programar o dispositivo e como integrá-lo com a blockchain.

## **Modelo de negócio da Tuya**
O Protocolo Shiva-esp8266 Blockchain também incorpora o modelo de negócio da Tuya, fornecendo uma plataforma fácil de usar para gerenciar dispositivos IoT. Os usuários podem criar dashboards personalizados e alertas de acordo com suas necessidades específicas, tornando a monitoração e controle das condições de uma estufa mais eficiente e eficaz.

## 1 - [IOT] Construindo, Conectando, Enviando Dados, Recebendo Dados, Executando ações.

Como construir, conectar, enviar e receber dados, e executar ações em um microcontrolador de forma segura. É apresentado um modelo padrão para programação em micropython, além de ensinar como conectar dispositivos de telemetria, como temperatura, umidade do ar, umidade do solo e quantidade de luz, para obter dados em tempo real. Também é abordado como conectar um umidificador para regular a umidade do ar e configurar comandos para execução de tarefas agendadas. O capítulo finaliza com dicas de segurança, abordando a autenticação SSL e explicando o que é chave pública e privada.

![+](./capitulo_1.md)

## 2 - [Blockchain] 

Para integrar dispositivo IOT com a Web3, usamos contratos inteligentes para registrar e gerenciar os dispositivos. Aqui estão os passos básicos para implementar um modelo de integração IOT com Web3:

### **Desenvolver o Smart Contract:** 

O primeiro passo é definir um contrato inteligente que será responsável por gerenciar os dispositivos IOT. O contrato deve ter as seguintes funcionalidades:

> ### **Registrar novos dispositivos:** 

permitir que novos dispositivos IOT sejam registrados na blockchain. Isso pode ser feito através de uma transação que inclui os dados do dispositivo, como seu endereço MAC, nome, localização e outros dados relevantes.

> ### **Gerenciar dispositivos:** 

permitir que os dispositivos sejam gerenciados através do contrato, como atualizar as informações do dispositivo, verificar se está ativo, etc.
Emitir alertas: permitir que o contrato emita alertas para os proprietários de dispositivos em caso de falhas ou outros eventos relevantes.

## ** Interface de usuário:** 

Para que os usuários possam interagir com o contrato, temos interface de usuário (UI). 

Atualmente : 

WEB > Gestão de acesso / Gestão de dispositivos / Dashboards

MOBILE > Telemetria / Agendamento de ações / Monitorações

## **Integrar o dispositivo IOT com o contrato:** 

O dispositivo IOT deve ser programado para se comunicar com o contrato, enviando informações sobre suas leituras de sensores para o contrato e recebendo comandos do contrato, como atualizações de configurações ou alertas.

Para se conectar na Ethereum e chamar um método de um contrato utilizando a biblioteca Micropython, é necessário instalar a biblioteca web3.py e importar as funções necessárias.

Vamos supor que o contrato que queremos interagir possui o seguinte método:

``` solidity

function setStatus(string memory _status) public {
    status = _status;
}

```

E que queremos chamar este método passando a string "Hello, world!" como parâmetro.

Segue abaixo um exemplo de código em Micropython que realiza essa operação:

``` python

from umqtt.simple import MQTTClient
from machine import Pin
import time
import urequests
import json
from web3 import Web3

# Configurações do dispositivo
SERVER = "mqtt.example.com"
CLIENT_ID = "esp8266_1"
TOPIC = b"device/data"
DHT_PIN = 2

# Configurações do contrato
CONTRACT_ADDRESS = "0x1234567890abcdef"
ABI = json.loads('[{"constant":false,"inputs":[{"name":"_status","type":"string"}],"name":"setStatus","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getStatus","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')

# Conexão com a blockchain
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/PROJECT_ID"))

# Conta para assinar transações
ACCOUNT_ADDRESS = "0x0123456789abcdef"
ACCOUNT_KEY = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

# Instancia o contrato
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# Conecta com o MQTT Broker
client = MQTTClient(CLIENT_ID, SERVER)
client.connect()

while True:
    # Lê os dados dos sensores
    temp = 25
    humidity = 50
    
    # Publica os dados no tópico MQTT
    data = {"temperature": temp, "humidity": humidity}
    payload = json.dumps(data)
    client.publish(TOPIC, payload)
    
    # Chama o método do contrato para atualizar o status
    status = "Hello, world!"
    nonce = w3.eth.getTransactionCount(ACCOUNT_ADDRESS)
    tx = contract.functions.setStatus(status).buildTransaction({
        'from': ACCOUNT_ADDRESS,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.toWei('40', 'gwei')
    })
    signed_tx = w3.eth.account.signTransaction(tx, private_key=ACCOUNT_KEY)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
    # Espera 1 minuto até a próxima leitura
    time.sleep(60)

``` 

Neste exemplo, é criada uma instância do contrato a partir do endereço e do ABI. Depois, é definida a conta que será utilizada para assinar as transações, bem como a chave privada correspondente.

O método setStatus é chamado passando a string "Hello, world!" como parâmetro. Para que a transação seja confirmada, é necessário definir o nonce e o gas adequados. Em seguida, a transação é assinada e enviada para a rede Ethereum.

Por fim, o dispositivo aguarda 1 min

## **Integrar a interface de usuário com o contrato:** 

A interface de usuário deve ser integrada com o contrato para permitir que os usuários visualizem as informações do dispositivo e gerenciem seus dispositivos.


## Testar e implantar: Após a conclusão do desenvolvimento, o contrato e a UI devem ser testados para garantir que estejam funcionando corretamente. Em seguida, eles podem ser implantados na blockchain para que os usuários possam começar a usá-los.



