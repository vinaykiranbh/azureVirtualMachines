try:
    import os
    import sys
    import boto3
    import json
    import time
    import botocore
    from boto3.dynamodb.conditions import Key
except ModuleNotFoundError:
    os.system('pip3 install boto3')

db = boto3.resource('dynamodb')

def main():

    try:
        # create a table
        response = db.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'CourseID',
                    'AttributeType': 'N'
                }
            ],
            TableName='Courses',
            KeySchema=[
                {
                    'AttributeName': 'CourseID',
                    'KeyType': 'HASH'
                }
            ],
            BillingMode='PAY_PER_REQUEST',

            TableClass='STANDARD'
        )
        print('Table Created Successfully.')
        
        # add 10 items to db
        time.sleep(10)
        
        
        return response
        
        
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ResourceInUseException':
            if error.response['Error']['Message'] == 'Table already exists: Courses':
                print('Table already exists: Courses')
        else:
            raise error
        

def addItems():
    table = db.Table('Courses')
    with open('courses.json', 'r') as f: 
        file = json.load(f)
    f.close()
    data = file['Courses']
    for i in range(0, len(data)):
        table.put_item(
            Item={
                "CourseID": data[i]['CourseID'],
                "NumCredits": data[i]['NumCredits'],
                "Title": data[i]['Title'],
                "CatalogNbr": data[i]['CatalogNbr'],
                "Subject": data[i]['Subject']
            }
        )
        print(f'Item {i} Created Successfully.')
    
    return 

def query():
    
    try:
        
        table = db.Table('Courses')
        print('Enter the Subject:')
        subject = str(sys.stdin.readline().strip())
        while subject == "":
            print('Please re-enter the Subject:')
            subject = str(sys.stdin.readline().strip())

        print('Enter the CatalogNbr:')
        cat = int(sys.stdin.readline().strip())
        while subject == "":
            print('Please re-enter the CatalogNbr:')
            cat = int(sys.stdin.readline().strip())

        res = table.scan(
            FilterExpression=Key("Subject").eq(subject) and Key("CatalogNbr").eq(cat)
        )
        
        if res['Items'] != []:
            print("The Title of Subject : {} and Catalog number: {} is {}".format(
                subject, cat, res['Items'][0]['Title']))
        else:
            print('No Title found for Subject : {} and Catalog number: {}'.format(
                subject, cat))

        print('Would you like to search for another title? (Y/N) ')
        ans = str(sys.stdin.readline().strip())
        while ans == "":
            print('Please re-enter your response:')
            ans = str(sys.stdin.readline().strip())

        return ans

    except botocore.exceptions.ClientError as error:
        raise error

    except botocore.exceptions.ParamValidationError as error:
        raise ValueError(
            'The parameters you provided are incorrect: {}'.format(error))


if __name__ == "__main__":
    
    main()
    addItems()
    ans = query()

    if ans == "Y":
        query()
    else:
        print('Thanks for using the Catalog Search program.')
