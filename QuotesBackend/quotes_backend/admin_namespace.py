import http.client

admin_namespace = Namespace('admin', description='Admin operations')


@admin_namespace.route('/quotes/<int:quote_id>/')
class QuotesDelete(Resource):

    @admin_namespace.doc('delete_quote',
                        responses={http.client.NO_CONTENT: 'No Content'})
    def delete(self, quote_id):
        '''
        Delete a quote
        '''
        quote = QuoteModel.query.get(quote_id)
        if not quote:
            # The quote is not present 
            return '', http.client.NO_CONTENT

        db.session.delete(quote)
        db.session.commit()

        return '', http.client.NO_CONTENT