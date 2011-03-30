import redis
#db = redis.new
db = redis.Redis(host='localhost', port=6379, db=0)
db.set('foo', 'bar')
print db.get('foo')

