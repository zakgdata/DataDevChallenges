import pandas as pd
import logging
import requests
import tableauserverclient as TSC
import smtplib

tableau_auth = TSC.TableauAuth('Your_Login', 'Your_Password', 'Your_Site')
server = TSC.Server('Your_Server')
logging.basicConfig(level='INFO')
server.version = '3.7'

def main():
    #TABLEAU METADATA QUERY
    query = """
        {
        fields{
            name
            datasource{
                downstreamOwners{
                    email
                }
            }
        }
    }
    """
    #AUTHENTICATE WITH TABLEAU SERVER
    with server.auth.sign_in(tableau_auth):
        resp = server.metadata.query(query)
        datasources = resp['data']
    
    #CONVERT DATA INTO DATAFRAME
    db_servers_df = pd.DataFrame(datasources['fields'])
    b = db_servers_df[db_servers_df['name'].isin(['Calculation1', 'Calculation2', 'Calculation3', 'Calculation4', 'Calculation5', 'Calculation6', 'Calculation7', 'Calculation8', 'Calculation9', 'Calculation10',
        'Test1', 'Test2', 'Test3', 'Test4', 'Test5', 'Test6', 'Test7', 'Test8', 'Test9', 'Test10'])]
    b['datasource'] = b['datasource'].astype(str).str.replace("\{\'downstreamOwners\'\: \[\{\'email\'\: \'", '')
    b['datasource'] = b['datasource'].astype(str).str.replace("\'\}\]\}", '')
    b = b.rename(columns={"name": "Field", "datasource": "Email"})
    
    #GENERATE EMAIL TO ASSOCIATED EMAIL
    i=0    
    for row in b:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login('Your_Email', '')
            subject = 'Poorly Named Field - ' + b.iat[i,0]
            body = 'Hello!\n\nPlease consider updating this field name to something more fitting: {}\n\nThanks, \nYour friendly neighborhood Tableau Admin'.format(b.iat[i,0])
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail('Your_Email', b.iat[i,1], msg)
            i += 1

            
if __name__ == '__main__':
    main()
