import http.client
from datetime import datetime
from flask_restx import Resource, fields, Namespace
from quotes_backend import config
from quotes_backend.models import QuoteModel
from quotes_backend.token_validation import validate_token_header
from quotes_backend.db import db 
from flask import abort


api_namespace = Namespace('api', description='API operations')


def authentication_header_parser(value):
    username = validate_token_header(value, config.PUBLIC_KEY)
    if username is None:
        abort(401)
    return username

# Input and output formats for Quote

authentication_parser = api_namespace.parser()
authentication_parser.add_argument('Authorization', location='headers',
                                   type = str, 
                                   help = 'Bearer Access Token')

quote_parser = authentication_parser.copy()
quote_parser.add_argument('text',type=str, required=True, help='Text of the Quote')

model = {
    'id': fields.Integer(),
    'username': fields.String(),
    'text': fields.String(),
    'timestamp': fields.DateTime(),
}
quote_model = api_namespace.model('Quote', model)


@api_namespace.route('/me/quotes/')
class MeQuoteListCreate(Resource):

    @api_namespace.doc('list_quotes')
    @api_namespace.expect(authentication_parser)
    @api_namespace.marshal_with(quote_model, as_list=True)
    def get(self):
        '''
        Retrieves all the quotes
        '''
        args = authentication_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])

        quotes = ( QuoteModel
                   .query
                   .filter(QuoteModel.username==username)
                   .order_by('id')
                   .all())
        return quotes

    @api_namespace.doc('create_quote') 
    @api_namespace.expect(quote_parser)
    @api_namespace.marshal_with(quote_model, code=http.client.CREATED)
    def post(self):
        '''
        create a quote
        '''
        args = quote_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])

        new_quote = QuoteModel(username=username,
                               text=args['text'],
                               timestamp=datetime.utcnow())
        db.session.add(new_quote)
        db.session.commit()

        result = api_namespace.marshal(new_quote, quote_model)

        return result, http.client.CREATED
        

search_parser = api_namespace.parser()
search_parser.add_argument('search', type=str,required=False,
                            help='search in the text of quotes')


@api_namespace.route('/quotes/')
class QuoteList(Resource):

    @api_namespace.doc('list_quotes')
    @api_namespace.marshal_with(quote_model, as_list=True)
    @api_namespace.expect(search_parser)
    def get(self):
        '''
        Retrieves all the quotes
        '''
        args = search_parser.parse_args()
        search_param = args['search']
        query = QuoteModel.query
        if search_param:
            param = f'%{search_param}%'
            query = (query.filter(QuoteModel.text.ilike(param)))
        
        query = query.order_by('id')
        quotes = query.all()

        return quotes

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