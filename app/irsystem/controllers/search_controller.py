from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import *


project_name = "Ilan's Cool Project Template"
net_id = "Ilan Filonenko: if56"


@irsystem.route('/', methods=['GET'])
def search():
	who = request.args.get('who')
	query = who
	occasion = request.args.get('occasion')
	min_price = request.args.get('min')
	max_price = request.args.get('max')

	if not who and not occasion:

		data = []
		output_message = ''
	else:
		query = query + occasion
		output_message = "Your search: " + query
		names, prices, ratings , url= calc_sort(doc_by_vocab,query,min_price,max_price)
		data = []
		for i in range(0,5):
			triplet = [names[i],prices[i],ratings[i],url[i]]
			data.append(triplet)
	return render_template('search.html', name=project_name, netid=net_id, output_message=query, data= data )
