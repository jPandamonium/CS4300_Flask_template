from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import *


project_name = "Ilan's Cool Project Template"
net_id = "Ilan Filonenko: if56"


@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search1')
	# query2 = request.args.get('search2')

	# if not query1 and not query2:
	# 	query = ""
	# if query1 and not query2:
	# 	query = query1 
	# elif query2 and not query1:
	# 	query = query2
	# else :
	# 	query = query1 + query2 
	if not query:
		data = []
		output_message = ''
	else:
		query = "calculator"
		output_message = "Your search: " + query
		data = calc_sort(doc_by_vocab,query)
	return render_template('search.html', name=project_name, netid=net_id, output_message=query, data=data)



