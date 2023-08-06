import iThenticate
client = iThenticate.API.Client('arham@chegg.com','Arham@2019')
client.login()

all_docs = client.documents.all('2320666','2')
print(all_docs)