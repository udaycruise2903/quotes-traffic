import http.client
from datetime import datetime
from flask_restplus import Namespace, Resource, fields

api_namespace = Namespace('api', description='API operations')

model = {
    'id': fields.Integer(),
    'username': fields.String(),
    'text': fields.String(),
    'timestamp': fields.DateTime(),
}
quote_model = api_namespace.model('Quote', model)


@api_namespace.route('/quotes/<int:quote_id>/')
class QuotesRetrieve(Resource):

    @api_namespace.doc('retrieve_quote')
    @api_namespace.marshal_with(quote_model)
    def get(self, quote_id):
        '''
        Retrieve a quote
        '''
        quote = QuoteModel.query.get(quote_id)
        if not quote:
            # The quote is not present
            return '', http.client.NOT_FOUND
        
        return quote