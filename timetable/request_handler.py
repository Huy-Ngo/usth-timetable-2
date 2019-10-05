from http import HTTPStatus as stat

dic = {
	stat.CREATED: 'Created',
	stat.NOT_FOUND: 'Not found',
	stat.BAD_REQUEST: 'Bad request',
	stat.FORBIDDEN: 'Forbidden',
	stat.OK: 'OK'
}


def handler(http_code, obj=None):
	message = dic[http_code]

	return {
		'code': http_code,
		'message': message,
		'response': obj
	}