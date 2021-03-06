import redis
import datetime
import time
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def redisWeekValidation( concept, user ):
	msg = ""
	r = redis.StrictRedis() # obtengo instancia de Redis	
	logger.info("redisWeekValidation(%i) => %s" % (user.id,concept))
	if r.exists(concept) != 0: # Si el concepto consultado ya existe (1 week), entonces no paga
		if r.exists("valordiario") == 0:
			prevuser = r.get(concept).decode("utf-8")
			msg = "El usuario @%s ya ha consultado por la definicion semanal '%s'\n\n" % (prevuser, concept.capitalize())
			msg += "!!*Aún puedes ganar la chaucha diaria*!!\n"
		msg += "!!*Busca una nueva definición y obtén tu chaucha diaria*!!\n\n" 

	return msg

def redisDayValidation( concept, user ):
	r = redis.StrictRedis() # obtengo instancia de Redis	
	if r.exists("valordiario") == 0: # Si el concepto diario no existe, se crea y paga
		now = datetime.datetime.now() # Ahora
		tomorrow = now + datetime.timedelta(days = 1) # Mañana
		week = now + datetime.timedelta(days = 7) # 1 Semana
		# Segundos hasta medianoche de mañana
		seconds_until_midnight = (tomorrow.replace(hour=0, minute=0, second=0, microsecond=0) - now).total_seconds()
		# Segundos hasta proxima semana
		seconds_until_oneweek_midnight = (week.replace(hour=0, minute=0, second=0, microsecond=0) - now).total_seconds()

		# Se obtienen valores enteros para pasarlos a Redis
		seconds_until_oneweek_midnight_int = int(round(seconds_until_oneweek_midnight))
		seconds_until_midnight_int = int(round(seconds_until_midnight)) 
		
		# Se guarda en la variable valordiario el username premiado del día
		logger.info("redisDayValidation(%i) => valor seconds diario [%i]" % (user.id,seconds_until_midnight_int))
		r.setex("valordiario", seconds_until_midnight_int, user.username) 
		# Se guarda en la variable concept el username premiado del día y se guarda 1 semana
		# Con esto evitamos que se consulte a diario por el concepto 'blockchain', forzando
		# la rotación de los diferentes conceptos
		logger.info("redisDayValidation(%i) => valor seconds week [%i]" % (user.id,seconds_until_oneweek_midnight_int))
		r.setex(concept, seconds_until_oneweek_midnight_int, user.username) 
		return True

	return False
