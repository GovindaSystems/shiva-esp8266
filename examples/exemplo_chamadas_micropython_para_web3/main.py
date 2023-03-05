# Importe as bibliotecas necessárias
import requests
import json
from umqtt.simple import MQTTClient
from web3 import Web3

# Configurações de conexão
ETH_NODE = "https://mainnet.infura.io/v3/YOUR-PROJECT-ID"
CONTRACT_ADDRESS = "0xYOUR-CONTRACT-ADDRESS"
ABI = json.loads('YOUR-CONTRACT-ABI')

# Cria a instância do Web3
w3 = Web3(Web3.HTTPProvider(ETH_NODE))

# Define a conta e a chave privada para assinar transações
ACCOUNT = w3.eth.account.from_key('YOUR-PRIVATE-KEY')

# Define o cliente MQTT
MQTT_SERVER = "YOUR-MQTT-SERVER"
MQTT_USER = "YOUR-MQTT-USER"
MQTT_PASS = "YOUR-MQTT-PASSWORD"
MQTT_TOPIC = "YOUR-MQTT-TOPIC"

# Conecta ao broker MQTT
mqtt = MQTTClient("client-id", MQTT_SERVER, user=MQTT_USER, password=MQTT_PASS)
mqtt.connect()

# Cria a instância do contrato
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# Define a função para chamar um método do contrato
def call_contract_method(method_name, *args):
    # Obtém a assinatura do método
    function = contract.functions[method_name](*args)
    # Obtém a transação não assinada
    txn = function.buildTransaction({'nonce': w3.eth.getTransactionCount(ACCOUNT.address)})
    # Assina a transação
    signed_txn = w3.eth.account.signTransaction(txn, ACCOUNT.privateKey)
    # Envia a transação assinada
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    # Aguarda a confirmação da transação
    receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    # Retorna o resultado da chamada do método
    return function.call({'from': ACCOUNT.address})

# Loop principal
while True:
    # Obtém os dados de telemetria
    temperature = read_temperature()
    humidity = read_humidity()
    # Chama o método do contrato para salvar os dados
    call_contract_method('saveTelemetry', temperature, humidity)
    # Publica os dados no broker MQTT
    mqtt.publish(MQTT_TOPIC, '{ "temperature": ' + str(temperature) + ', "humidity": ' + str(humidity) + ' }')
    # Aguarda 5 minutos
    time.sleep(300)