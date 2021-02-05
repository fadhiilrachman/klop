import requests, json, sys
# fill your cookie and token

class Instagram:
	_session	= requests.session()
	uname		= ''
	headers = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
		'cookie': 'YOUR INSTAGRAM COOKIE start with ig_did=....'
	}

	def __init__(self, uname):
		self.uname = uname

	def getProfile(self):
		api_url = 'https://www.instagram.com/%s/?__a=1' % (self.uname)
		headers = self.headers
		result_json = self._session.get(api_url, headers=headers)
		
		return json.loads(result_json.text)

	def getStockAndExchange(self):
		uri_stock = 'https://finnhub.io/api/v1/quote'
		stock_result_json = self._session.get(uri_stock, params={'token': 'YOUR FINNHUB TOKEN', 'symbol': 'FB'}, headers=self.headers)
		stock_res=json.loads(stock_result_json.text)
		stock = float(stock_res['o'])

		uri_exchange = 'https://api.exchangeratesapi.io/latest?base=USD'
		exchange_result_json = self._session.get(uri_exchange, headers=self.headers)
		exchange_res=json.loads(exchange_result_json.text)
		rates = float(exchange_res['rates']['IDR'])

		strtotal=((stock * 0.01) * rates)

		return strtotal

	# def scrapTimelineCounts(self, user_id, end_cursor):
	# 	status_loop = True
	# 	api_url = 'https://www.instagram.com/graphql/query/?query_id=17888483320059182&id=%s&first=12&after=%s' % (user_id, end_cursor)
	# 	headers = self.headers
	# 	sc_post_likes = 0
	# 	sc_post_comment = 0
	# 	while status_loop:
	# 		result_json = self._session.get(api_url, headers=headers)
	# 		data = json.loads(result_json.text)

	# 		if 'data' not in data:
	# 			status_loop = False
	# 		else:
	# 			has_next_page = data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
	# 			end_cursor = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

	# 			posts = data['data']['user']['edge_owner_to_timeline_media']['edges']
	# 			for i in posts:
	# 				sc_post_likes=int(sc_post_likes)+int(i['node']['edge_media_preview_like']['count'])
	# 				sc_post_comment=int(sc_post_comment)+int(i['node']['edge_media_to_comment']['count'])
				
	# 			if has_next_page == False:
	# 				status_loop = False

	# 	return [sc_post_likes, sc_post_comment]

	def human_format(self, num):
		num = float('{:.3g}'.format(num))
		magnitude = 0
		while abs(num) >= 1000:
			magnitude += 1
			num /= 1000.0
		return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

if len(sys.argv) > 1:
	username = sys.argv[1]

	ig = Instagram(username)
	data = ig.getProfile()
	user_id = data['graphql']['user']['id']
	followers = data['graphql']['user']['edge_followed_by']['count']
	profile_pic = data['graphql']['user']['profile_pic_url_hd']
	is_private = data['graphql']['user']['is_private']
	is_verified = data['graphql']['user']['is_verified']

	has_next_page = data['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
	end_cursor = data['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

	posts = data['graphql']['user']['edge_owner_to_timeline_media']['edges']

	total_post_likes=0
	total_post_comment=0

	stockexch=0
	score_likes=0
	score_comments=0
	score_followers=0
	score=0
	
	for i in posts:
		total_post_likes=int(total_post_likes)+int(i['node']['edge_liked_by']['count'])
		total_post_comment=int(total_post_comment)+int(i['node']['edge_media_to_comment']['count'])
		
	# if has_next_page != False:
	# 	total = ig.scrapTimelineCounts(user_id, end_cursor)
	# 	total_post_likes = total_post_likes+total[0]
	# 	total_post_comment = total_post_comment+total[1]

	stockexch = int(ig.getStockAndExchange())
	score_likes = int(total_post_likes * (0.001 * stockexch ) )
	score_comments = int(total_post_comment * (0.01 * stockexch ) )
	score_followers = int(followers * (0.001 * stockexch ) )
	score = score_likes + score_comments + score_followers
	if is_verified is True:
		score = int(score * (0.00005 * stockexch ) )
	if is_private is True:
		score = int(score * (0.00001 * stockexch ) )
	send = {
		'score': score,
		'profile_pic': profile_pic,
		'username': username,
		'kriteria': [
			'Memiliki %s likes terakhir' % ( ig.human_format(total_post_likes) ),
			'Memiliki %s komentar terakhir' % ( ig.human_format(total_post_comment) ),
			'Memiliki %s followers akun' % ( ig.human_format(followers) )
		]
	}
	print( json.dumps(send) )
else:
	print("Username tidak ditemukan")
