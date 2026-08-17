dict(
    needs=dict(
        rdf1='''
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
        rdf2='''
        ''',
        proposal=''' #todo
            [a :Person, :user; :name "anhi"] :yr [a ]
        ''',
        short='''
        ''',
    ),
)
