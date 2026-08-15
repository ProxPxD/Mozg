dict(
    needs=dict(
        rdf='''
            _:anhi 
                a :user, :Person ;
                :eq 'Anhi' ;
                :yr _:buys .
            _:needs 
                a :action ;
                :eq 'need' ;
                :ry _:anhi ;
                :rj _:buy . 
            _:buys
                a :action ;
                :eq 'buy' ;
                :rj _:product . 
            _:product
                :eq 'sauce'.
        ''',
        proposal='''
            [a :Person, :user; :name "anhi"] :yr [a ]
        '''
        short='''
        '''
    )
)