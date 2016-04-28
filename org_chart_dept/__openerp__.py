{
    'name': 'Department Hierarchy',
    'category': 'Website',
    'summary': 'To display Departments in Hierarchical Manner',
    'website': 'https://www.credativ.in',
    'version': '1.0',
    'description': """
        """,
    'author': 'Murali Krishna Reddy',
    'depends': ['base','website','hr'],     
    'sequence':0,   
    'images':['images/org1.png'],
    'data': [    
        'views/website_dept_chart_backend.xml',
        'views/website_dept_chart.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
