## **Overview**

The dynamodb suite of commands from the AWS CLI does not support a document-interface, where you can specify attribute values without the use of data type descriptors. This CLI tool provides a document interface for all API parameters by leveraging boto3's document interface (service resource).



## **Installation**

`pip install dynode -U`

### **from source**

`git clone https://github.com/knavsaria/dynodoc ; cd dynodoc`

`pip install -e .`



### auto-complete

To enable auto-complete, add the following line to ~/.bashrc

`eval "$(_DYNODOC_COMPLETE=source dynodoc)"`



## Examples



`dynodoc create-table --name tester --num-hash countryCode --str-sort surname`

`dynodoc put-item --name tester --item '{"countryCode":27, "surname": "navsaria"}' --condition-expression 'attribute_not_exists(id)' --show-capacity TOTAL`

`dynodoc get-item --name tester --num-hash countryCode 27 --str-sort surname navsaria`

`dynodoc query --name tester --key-condition-expression '#country = :rsa' --expression-attribute-names '{"#country":"countryCode"}' --expression-attribute-values '{":rsa": 27}'`

`dynodoc update-item --name tester --num-hash countryCode 27 --str-sort surname navsaria --update-expression 'SET #firstname = :name' --condition-expression '#country = :rsa' --expression-attribute-names '{"#country": "countryCode", "#firstname": "firstname"}' --expression-attribute-values '{":name": "keeran", ":rsa": 27}'`

 
