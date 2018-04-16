from config import salt, satoshi, fee, magic
from requests import get, post
from bitcoin import *
import binascii
import time

def getTx(addr):
	info = get('http://insight.chaucha.cl/api/txs/?address=' + addr).json()
	msg = ''
	totalPages = range(int(info['pagesTotal']))
	# para prevenir que se busque en todas las paginas. Debería buscar las ultimas 1 o 2 (codigo no probado)
	if totalPages > 2:
		totalPages = 2

	for x in totalPages:
		info = get('http://insight.chaucha.cl/api/txs/?address=' + addr + '&pageNum=' + str(x)).json()
		for i in info['txs']:
			for j in i['vout']:
				hex_script = j['scriptPubKey']['hex']
				if hex_script[:2] == '6a':
					if len(hex_script) <= 77*2:
						sub_script = hex_script[4:]
					else:
						sub_script = hex_script[6:]

					msg_str = binascii.a2b_hex(sub_script).decode('utf-8', errors='ignore')
					fecha = time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(int(i['time'])))

					if not msg_str == 'Quirquincho':
						msg += '[' + fecha +'](http://insight.chaucha.cl/tx/' + i['txid'] + '): `' +  msg_str + '`\n'
	return msg


def OP_RETURN_payload(string):
	metadata = bytes(string, 'utf-8')
	metadata_len= len(metadata)
	
	if metadata_len<=75:
		payload=bytearray((metadata_len,))+metadata # length byte + data (https://en.bitcoin.it/wiki/Script)
	elif metadata_len<=256:
		payload=b"\x4c"+bytearray((metadata_len,))+metadata # OP_PUSHDATA1 format
	else:
		payload=b"\x4d"+bytearray((metadata_len%256,))+bytearray((int(metadata_len/256),))+metadata # OP_PUSHDATA2 format

	return payload

def sendTx(info, amount, receptor, op_return):
		addr = info[0]
		privkey = info[1]
		
		info = getbalance(addr)
		confirmed_balance = info[0]
		inputs = info[1]

		if not len(receptor) == 34 and receptor[0] == 'c':
			msg = "Dirección inválida"

		elif not confirmed_balance >= amount:
			msg = "Balance insuficiente"

		elif not amount > 0:
			msg = "Monto inválido"

		else:
			# Transformar valores a Chatoshis
			used_amount = int(amount*satoshi)
			used_fee = int(fee*satoshi)

			# Utilizar solo las unspent que se necesiten
			used_balance = 0
			used_inputs = []

			for i in inputs:
				used_balance += i['value']
				used_inputs.append(i)
				if used_balance > used_amount:
					break

			# OP_RETURN
			payload = OP_RETURN_payload(op_return)
			script = '6a' + binascii.b2a_hex(payload).decode('utf-8', errors='ignore')

			# Creación de salida
			if used_amount == used_balance:
				outputs = [{'address' : receptor, 'value' : (used_amount - used_fee)}, {'value' : 0, 'script' : script}]
			else:
				outputs = [{'address' : receptor, 'value' : used_amount}, {'address' : addr, 'value' : int(used_balance - used_amount - used_fee)}, {'value' : 0, 'script' : script}]

			# Transacción
			tx = mktx(used_inputs, outputs)

			# Firma
			for i in range(len(used_inputs)):
				tx = sign(tx, i, privkey)

			broadcasting = post('http://insight.chaucha.cl/api/tx/send', data={'rawtx' : tx})

			try:
				msg = "insight.chaucha.cl/tx/%s" % broadcasting.json()['txid']
			except:
				msg = broadcasting.text
			
		return msg


def getaddress(user_id):
	privkey = sha256(str(user_id) + str(salt))
	addr = privtoaddr(privkey, magic)
	return [addr, privkey]

def getbalance(addr):
	# Captura de balance por tx sin gastar
	unspent = get('http://insight.chaucha.cl/api/addr/' + addr + '/utxo').json()
		
	confirmed = unconfirmed = 0

	inputs = []
	for i in unspent:
		if i['confirmations'] >= 6:
			confirmed += i['amount']
			inputs_tx = {'output' : i['txid'] + ':' + str(i['vout']), 'value' : i['satoshis'], 'address' : i['address']}
			inputs.append(inputs_tx)
		else:
			unconfirmed += i['amount']

	return [confirmed, inputs, unconfirmed]
