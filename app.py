# Run this app with `python app.py` and


from dash import Dash, dcc, html, Input, Output, State, dash_table
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import json
import pymysql

def connect():
    return pymysql.connect(host = "database-1.c1t73pyaszrz.us-west-1.rds.amazonaws.com", port = int(3306), user = "admin", password = "12345678", database = "AcademicWorld") 

app = Dash(__name__)
db = connect()
cursor = db.cursor()
cursor.execute('call allKeywords()')
allKeywords = [column[0] for column in cursor.fetchall()]
cursor.execute('call allUniversity()')
allUniversities = [column[0] for column in cursor.fetchall()]

# Figure 1 
cursor.execute("call findFacultyOfKeywordUniversity('computer vision', 'University of Illinois at Urbana Champaign')")
data1 = cursor.fetchall()
ids = [(str(column[0])) for column in data1]
professors = [column[1] for column in data1]
scores = [column[2] for column in data1]
keywords = [column[3] for column in data1]
universities = [column[4] for column in data1]
# enter your code here!
df1 = pd.DataFrame({
    "ProfessorId": ids,
    "Professor": professors,
    "Score": scores,
    "Keyword": keywords,
    "University": universities
})
fig1 = px.bar(df1, x="ProfessorId", y="Score", hover_data = ["Professor", "University", "Keyword"], color = 'Score')


# Figure 2
allYears = [i for i in range(2000, 2023)]
cursor.execute("call findPopularKeywordsAfterYear(2000)")
data2 = cursor.fetchall()
keyword_names = [column[0] for column in data2]
keyword_ids = [str(column[2]) for column in data2]
keyword_citation_number = [column[1] for column in data2]
df2 = pd.DataFrame({
    "KeywordId": keyword_ids,
    "Keyword": keyword_names,
    "Citations": keyword_citation_number,
})
fig2 = px.bar(df2, x="KeywordId", y="Citations", hover_data = ["Keyword"], color = 'Citations')



# Figure 3
cursor.execute("call findUniversityFacultyCntByLikeKeyword('data')")
data3 = cursor.fetchall()
university_names3 = [column[0] for column in data3]
faculty_count = [str(column[1]) for column in data3]
university_ids3 = [str(column[2]) for column in data3]
df3 = pd.DataFrame({
    "UniversityId": university_ids3,
    "University": university_names3,
    "Faculty_count": faculty_count,
})
fig3 = px.bar(df3, x="UniversityId", y="Faculty_count", hover_data = ["University"], color = 'Faculty_count')

# # Figure 4
query = "select * from v1"
cursor.execute(query)
data4 = cursor.fetchall()
university_names4 = [column[0] for column in data4]
publication_count4 = [str(column[3]) for column in data4]
faculty_names4 = [column[2] for column in data4]
faculty_ids4 = [str(column[1]) for column in data4]
df4 = pd.DataFrame({
    "University": university_names4,
    "Publication_count": publication_count4,
    "ProfessorId": faculty_ids4,
    "Professor": faculty_names4
})
fig4 = px.bar(df4, x="ProfessorId", y="Publication_count", hover_data = ["Professor", "University"], color = 'Publication_count')

# Figure 5
query = "select faculty.id, faculty.name from faculty;"
cursor.execute(query)
data5 = cursor.fetchall()

faculty_info = ['{{"Id":{0},"Name":"{1}"}}'.format(str(column[0]), column[1]) for column in data5]
currentId = -1

# Figure 6
current_univerisityId = -1

db.close()

app.layout = html.Div(children=[
    html.Div(
        children=[
            html.H1(
                children="AcademicWorld",style={'textAlign': 'center'}, className="header-title" 
            ), #Header title
        ],
        className="header",style={'backgroundColor':'#F5F5F5'},
    ), #Description below the header

    html.Div(
        children=[
            html.Div(
                children = [
                    html.H4(id = 'title1', children="Top 10 faculty members who are relevant to 'computer vision' in 'University of Illinois at Urbana Champign'"),
                    html.Div([
                        html.Div(
                            html.P(children = '''University:'''),
                            style={'width': '20%', 'display': 'inline-block'},
                        ),
                        html.Div(
                            dcc.Dropdown(allUniversities, id='university1', style={'height': '15px', 'width': '350px', 'fontSize': '16px'}),
                            style={'width': '80%', 'display': 'inline-block'},
                        ),
                    ]),
                    html.Div([
                        html.Div(
                            html.P(children = '''Keyword:'''),
                            style={'width': '20%', 'display': 'inline-block'},
                        ),
                        html.Div(
                            dcc.Dropdown(allKeywords, id='keyword1', style={'height': '15px', 'width': '350px', 'fontSize': '16px'}),
                            style={'width': '80%', 'display': 'inline-block'},
                        ),
                    ]),
                    html.Button('Submit', id='submit-val', n_clicks = 0),
                    html.P(id = 'prompt1'),
                    dcc.Graph(
                        id = 'u1',
                        figure = fig1,
                        #config={"displayModeBar": False},
                    ),
                ],
                style={'width': '33%', 'display': 'inline-block'},
            ),
            html.Div(
                children = [
                    html.H4(id = 'title2', children="Top 10 most popular keywords among publications that were published in or after year 2000"),
                    html.Br(),
                    html.Br(),
                    
                    html.Div([
                        html.Div(
                            html.P(children = '''Year:'''),
                            style={'width': '20%', 'display': 'inline-block'},
                        ),
                        html.Div(
                            dcc.Dropdown(allYears, allYears[0], id='year2', style={'height': '15px', 'width': '350px'}),
                            style={'width': '80%', 'display': 'inline-block'},
                        ),
                    ]),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    
                    dcc.Graph(
                        id = 'u2',
                        figure = fig2,
                        #config={"displayModeBar": False},
                    ),
                ],
                style={'width': '33%', 'display': 'inline-block'},
            ),
            html.Div(
                children = [
                    html.H4(id = 'title3', children="Top 10 universities that have the most faculty members researching on 'data' related topics"),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        "Input: ",
                        dcc.Input(id='input3', type='text'),
                        html.Button('Submit', id='submit3', n_clicks=0),
                    ]),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(
                        id = 'u3',
                        figure = fig3,
                        #config={"displayModeBar": False},
                    ),
                ],
                style={'width': '34%', 'display': 'inline-block'},
            ),
            html.Div(
                children = [
                    html.H4(id = "title4", children=''' Top 10 faculty members who have the largest number of publications '''),
                    dcc.Graph(
                        id = 'u4',
                        figure = fig4,
                        #config={"displayModeBar": False},
                    ),
                    html.Br(),
                ],
                
                style={'width': '33%', 'display': 'inline-block'},
            ),
            html.Div(
                children = [
                    html.Div([
                        html.H4(children=''' Faculty Search '''),
                        html.Div(
                            html.P('''Info:'''),
                            style={'width': '10%', 'display': 'inline-block'},
                        ),
                        html.Div(
                            dcc.Dropdown(faculty_info, id='info5', style={'height': '30px', 'width': '400px'}),
                            style={'width': '90%', 'display': 'inline-block'},
                        ),
                    ]),
                    html.P(id = 'prompt5'),
                    html.Div(
                        children = [
                            html.Div([
                                html.P(id='fid1', children="Faculty Id: "),
                            ]),
                            html.Br(),
                            html.Div([
                                html.P(id='fn1', children="Faculty Full Name: ")
                                
                            ]),
                            html.Br(),
                            html.Div([
                                "University: ",
                                dcc.Input(id='un2', type='text'),
                                html.Div(id='un1'),
                                
                            ]),
                            html.Br(),
                            html.Div([
                                "Phone Number: ",
                                dcc.Input(id='pn2', type='text'),
                                html.Div(id='pn1'),
                                
                            ]),
                            html.Br(),
                            html.Div([
                                "Position: ",
                                dcc.Input(id='po2', type='text'),
                                html.Div(id='po1'),
                                
                            ]),
                            html.Br(),
                            html.Div([
                                "Research Interest: ",
                                dcc.Input(id='ri2', type='text'),
                                html.Div(id='ri1'),
                                
                            ]),
                            html.Br(),
                            html.Div([
                                "Email: ",
                                dcc.Input(id='em2', type='text'),
                                html.Div(id='em1'),
                                
                            ]),
                            html.Br(),
                            html.Button('Update Faculty Info', id='update', n_clicks=0),
                            html.Br(),html.Br(),
                        ]
                        
                    )

                ],
                style={'width': '33%', 'display': 'inline-block'},
            ),
            html.Div(
                children = [
                    html.Div([
                        html.H4(children=''' University Search '''),
                        html.Br(),
                        html.Div(
                            html.P('''Info:'''),
                            style={'width': '10%', 'display': 'inline-block'},
                        ),
                        html.Div(
                            dcc.Dropdown(allUniversities, id='university6', style={'height': '30px', 'width': '400px'}),
                            style={'width': '90%', 'display': 'inline-block'},
                        ),
                    ]),
                    html.P(id = 'prompt6'),
                    html.Div(
                        children = [
                            html.Div([
                                html.P(id='uniId1', children="University Id: "),
                            ]),
                            html.Br(),
                            html.Div([
                                "University: ",
                                dcc.Input(id='uname2', type='text'),
                                html.Div(id='uname1'),
                            ]),
                            html.Br(),
                            html.Div([
                                "Photo_URL: ",
                                dcc.Input(id='ph2', type='text'),
                                html.Div(id='ph1'),  
                            ]),
                            html.Br(),
                            html.Div([
                                html.P(id='nf1', children="Number of faculty: "),
                            ]),
                            html.Br(),
                            html.Button('Update University Info', id='update2', n_clicks=0),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
                            
                        ]
                        
                    )

                ],
                style={'width': '33%', 'display': 'inline-block'},
            ),     
        ],
        className = 'double-graph',
        style = {'display': 'inline-block'}
        ), 
    ]
 #Four graphs
)

# fig1
@app.callback(
    Output("u1", "figure"),
    State("university1", "value"), 
    State("keyword1", "value"),
    Input("submit-val", "n_clicks"), 
)
def update_fig1(a, b, c):
    if b is None:
        raise PreventUpdate
    elif a is None:
        query = "call findFacultyOfKeyword('computer vision')"
    else:    
        query = "call findFacultyOfKeywordUniversity('{0}', '{1}')".format(b, a)

    db = connect()
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    ids = [str(column[0]) for column in data]
    professors = [column[1] for column in data]
    scores = [column[2] for column in data]
    keywords = [column[3] for column in data]
    universities = [column[4] for column in data]
    # enter your code here!
    df = pd.DataFrame({
        "ProfessorId": ids,
        "Professor": professors,
        "Score": scores,
        "Keyword": keywords,
        "University": universities
    })
    fig1 = px.bar(df, x="ProfessorId", y="Score", hover_data = ["Professor", "University", "Keyword"], color = 'Score')
    return fig1

@app.callback(
    Output("prompt1", "children"),
    State("university1", "value"), 
    State("keyword1", "value"),
    Input("submit-val", "n_clicks"), 
)
def update_prompt1(a, b, c):
    if b is None:
        return 'A keyword is required'
    else:
        return "Query executed successfully"

@app.callback(
    Output("title1", "children"),
    State("university1", "value"), 
    State("keyword1", "value"),
    Input("submit-val", "n_clicks"), 
)
def update_title1(a, b, c):
    if b is None:
        raise PreventUpdate
    if a is None:
        return "Top 10 faculty members who are relevant to '{0}'".format(b)
    else:
        return "Top 10 faculty members who are relevant to '{0}' in '{1}'".format(b, a)

# fig2
@app.callback(
    Output("u2", "figure"),
    Input("year2", "value"), 
)
def update_fig2(value):
    if value is None:
        raise PreventUpdate
    db = connect()
    cursor = db.cursor()
    cursor.execute("call findPopularKeywordsAfterYear({0})".format(value))
    data2 = cursor.fetchall()
    cursor.close()
    db.close()
    keyword_names = [column[0] for column in data2]
    keyword_ids = [str(column[2]) for column in data2]
    keyword_citation_number = [column[1] for column in data2]
    df2 = pd.DataFrame({
        "KeywordId": keyword_ids,
        "Keyword": keyword_names,
        "Citations": keyword_citation_number,
    })
    fig2 = px.bar(df2, x="KeywordId", y="Citations", hover_data = ["Keyword"], color = 'Citations')
    return fig2

@app.callback(
    Output("title2", "children"),
    Input("year2", "value"), 
)
def update_title2(value):
    if value is None:
        raise PreventUpdate
    return "Top 10 most popular keywords among publications that were published in or after year {0}".format(value)

# fig3
@app.callback(
    Output("u3", "figure"),
    Input('submit3', 'n_clicks'),
    State('input3', 'value') 
)
def update_fig3(n_clicks, value):
    if value is None:
        raise PreventUpdate
    db = connect()
    cursor = db.cursor()
    cursor.execute("call findUniversityFacultyCntByLikeKeyword('{0}')".format(value))
    data3 = cursor.fetchall()
    print(data3)
    university_names3 = [column[0] for column in data3]
    faculty_count = [str(column[1]) for column in data3]
    university_ids3 = [str(column[2]) for column in data3]
    df3 = pd.DataFrame({
        "UniversityId": university_ids3,
        "University": university_names3,
        "Faculty_count": faculty_count,
    })
    db.close()
    fig3 = px.bar(df3, x="UniversityId", y="Faculty_count", hover_data = ["University"], color = 'Faculty_count')
    return fig3

@app.callback(
    Output('fid1', 'children'),
    Output('fn1', 'children'),
    Output('un1', 'children'),
    Output('pn1', 'children'),
    Output('po1', 'children'),
    Output('ri1', 'children'),
    Output('em1', 'children'),
    Input('info5', 'value'),
)
def show_faculty(value):
    if value is None:
        raise PreventUpdate
    print("callback1")
    facultyId = json.loads(value)['Id']
    global currentId
    currentId = facultyId
    db = connect()
    cursor = db.cursor()
    cursor.execute("call findFacultyById({0},@fn,@un,@ph,@po,@ri,@em)".format(facultyId))
    cursor.execute("select @fn,@un,@ph,@po,@ri,@em")
    faculty = cursor.fetchone()
    print(faculty)
    return "Faculty Id: "+str(facultyId),"Faculty Full Name: "+faculty[0],faculty[1],faculty[2],faculty[3],faculty[4],faculty[5]        

@app.callback(
    Output('prompt5', 'children'),
    Input('update', 'n_clicks'),
    State('un2', 'value'),
    State('pn2', 'value'),
    State('po2', 'value'),
    State('ri2', 'value'),
    State('em2', 'value')
)
def update_title3(a, b, c, d, e, f):
    print("{0}{1}{2}{3}{4}".format(b,c,d,e,f))
    print("currentId is {0}".format(currentId))
    print(b)
    updateSegment = ""
    if b is not None:
        db = connect()
        cursor = db.cursor()
        cursor.execute("call findUniversityByName('{0}')".format(b))
        uni = cursor.fetchone()
        db.close()
        print(uni)
        if uni is None:
            return 'This university does not exist.'
        else:
            updateSegment += "university_id = {0},".format(uni[0])
    if c is not None:
        updateSegment += "phone = '{0}',".format(c)
    if d is not None:
        updateSegment += "position = '{0}',".format(d)
    if e is not None:
        updateSegment += "research_interest = '{0}',".format(e)
    if f is not None:
        updateSegment += "email = '{0}',".format(f) 
    if len(updateSegment) > 0:
        updateSegment = updateSegment[0:-1]
    else:
        return "No Update"    
    query = "update faculty set {0} where id = {1};".format(updateSegment, currentId)
    print(query)
    db = connect() 
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()
    return "Updated Successfully"
# fig6
@app.callback(
    Output('uniId1', 'children'),
    Output('uname1', 'children'),
    Output('ph1', 'children'),
    Output('nf1', 'children'),
    Input('university6', 'value'),
)
def show_university(value):
    print(value)
    if value is None:
        raise PreventUpdate
    print("callback1")
    global current_univerisityId
    db = connect()
    cursor = db.cursor()
    cursor.execute("call findUniversityByName('{0}')".format(value))
    faculty = cursor.fetchone()
    print(faculty)
    print("end")
    current_univerisityId = faculty[0]
    return "University Id: "+str(faculty[0]), faculty[1],faculty[2],"Number of faculty: "+str(faculty[3])        

@app.callback(
    Output('prompt6', 'children'),
    Input('update2', 'n_clicks'),
    State('uname2', 'value'),
    State('ph2', 'value'),
)
def update_title3(a, b, c):
    print("currentId is {0}".format(currentId))
    updateSegment = ""
    if b is not None:
        updateSegment += "name = '{0}',".format(b)
    if c is not None:
        updateSegment += "photo_url = '{0}',".format(c)
    if len(updateSegment) > 0:
        updateSegment = updateSegment[0:-1]
    else:
        return "No Update"    
    query = "update university set {0} where id = {1};".format(updateSegment, current_univerisityId)
    print(query)
    db = connect() 
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()
    return "Updated Successfully"                   




if __name__ == '__main__':
    app.run_server()




