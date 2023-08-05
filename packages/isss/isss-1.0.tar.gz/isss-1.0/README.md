# ISSS - A Python module for IBM Security Secret Server

The `isss` module is meant to be an abstract layer on top of the IBM Security Secret Server REST APIs.

It is **NOT** a full implementation of the REST APIs capabilities. It only provides wrappers for most useful scenarios, additionnal functions will appear from time to time.

Also, notice that you will use it at your own risk, as *it is not officially supported by IBM*

# Installation & pre-requisites

From a terminal, simply issue the following command : 

```
$ pip install isss
```

And that's all ! The library should work as-is. It should be OS independant too, but it's **compatible with Python 3.x only**

You can verify your installation by copy-pasting this line into a shell : 

```
$ python -c "import isss; print (isss.version)"
```

It should display your current isss version. If you've got an error complaining about several missing modules, it's probably a system config issue resulting in the old python 2.7 being run by default instead of python 3

Try to issue the same command, but using `python3` instead of `python` to force the use of python 3.x 

```
$ python3 -c "import isss; print (isss.version)"
```

# Current known limitations

Many ! Either because I'm lacking of time or because some REST APIs are simply not available (unlike their SOAP counterpart), you might find that the thing you want to achieve is not possible with the current version of the module. 

Non exhaustive list of missing features:

* Create or search secret policies (REST APIs seem not available)
* Advanced search (pagination, complex queries). Only per-id or global search text is available for most items (users, secrets, groups, folders) and only first 100 items are returned
* Checkin, checkout
* Recorded sessions
* Teams
* Workflows

This module is still a work in progress, though.

# Importing the module

Before using the module, you must import it (who knew?). The `isss` module contains a class named `ISSS` which contains everything you need. 

```python
from isss import ISSS
isss = ISSS("https://your.server.demo.com/SecretServer","admin","yourpassword")
```

# Stubs

A stub is basically a map of values that you can read, but also edit then push back to secret server to create or update a resource. You'll get a stub (or list of stubs) after a search, a create, or an update.

**Tip** : from an interactive shell, stubs can be pretty-printed to have a clear view of their content: 

```python
>>> u = isss.getUser(3)
>>> u
<User id='3' username='python' displayName='Python App' />
>>> print(u)
- id : 3
- userName : python
- displayName : Python App
- lastLogin : 2019-06-13T12:30:31
- created : 2019-06-11T09:14:12
- enabled : True
- loginFailures : 0
- emailAddress : None
- userLcid : 0
- domainId : -1
- lastSessionActivity : None
- isLockedOut : False
- radiusUserName : None
- twoFactor : False
- radiusTwoFactor : False
- isEmailVerified : False
- mustVerifyEmail : False
- verifyEmailSentDate : 0001-01-01T00:00:00
- passwordLastChanged : 0001-01-01T00:00:00
- dateOptionId : -1
- timeOptionId : -1
- isEmailCopiedFromAD : False
- organizationUnitId : -1
- adGuid : None
- adAccountExpires : 0001-01-01T00:00:00
- resetSessionStarted : 0001-01-01T00:00:00
- isApplicationAccount : True
- oathTwoFactor : False
- oathVerified : False
- duoTwoFactor : False
- fido2TwoFactor : False
- password : None
>>> 

```

**Tip**: The variables inside a stub are case-insensitive.

```python
stub["username"] = "romain"
stub["userName"] = "romain" #similar to the previous line
```

Of course, accessing an unknown variable inside the stub will raise an exception.

Each stub will also have a _create()_ and _update()_ method, in order to be pushed back to Secret Server. 

It's now time to read the examples below to have a better understanding of the concept.



# Doing some searches

Each time you'll search for something, you'll get a stub if you pass a numerical id, or a _list of stubs_ if you pass a string query. 


### Searching secrets

```python
for s in isss.getSecret("centos root account"):
    print (s['id'])
```

or get a specific secret, using a secret ID

```python
print (isss.getSecret(2))
```


### Searching users

```python
for u in isss.getUser("admin"):
    print (u['id'])
```

...or get a specific user, using a user ID

```python
print (isss.getUser(2))
```

### Searching groups (and adding users into a group)
```python
for g in isss.getGroup("Users"):
    print (g['id'])
```

...or get a specific group, using a group ID
```python
print (isss.getGroup(2))
```

### Searching folders

```python
for f in isss.getFolder("Windows Systems"):
    print (f['id'])
```

...or get a specific folder, using a folder ID
```python
print (isss.getFolder(2))
```

### Searching templates
```python
for t in isss.getTemplate("Unix Account (SSH)")
   print ("Template id found : "), (t["id"])
```

...or get a specific template, using a template ID
```python
template = isss.getTemplate(6007)
```

# Creating things

To create something, you'll need an empty stub of this particular something. Once you've got a stub, edit the stub then call its create() method.

### Creating a secret

```python
#To create a new secret, grab a template id first
myid = isss.getTemplates("Unix Account (SSH)")[0]["id"]

#Then grab the corresponding secret stub
#which contains basically all the default values for this template.
stub = isss.getSecretStub(myid) 

#Then edit these values. Be careful, some of them might be mandatory 
#Typically 'name' which is the secret name
#Developer tip : these fields are case insensitive

stub["name"] = "python\\foobar.demo.com"
stub["machine"] = "foobar.demo.com"
stub["username"] = "root"
stub["password"] = stub.generatePassword()
stub["folderId"] = isss.getFolders("Linux")[0]["id"]
stub["enableInheritPermissions"] = False #important for the next sample

#Display a nice listing of all the available fields and their current value
#This is useful when playing live with the module
print (stub) 

#Then finally create the secret, and keep a reference
#We'll need it very soon
secret = stub.create()
```

Pay attention to the use of the generatePassword() method in the previous example. 

This method is only available on stub object, because each secret field can have its own secret policy.

This is why you also might need to specify the name of the field as a parameter so that the method will generate a valid password for the associated field. 

For convenient reason, default field name is set to `"password"`.

```python
# private key passphrase may require a longer password
stub["Private Key Passphrase"] = stub.generatePassword("Private Key Passphrase")
```

### Creating a secret permission

To create a new permission for a specific secret, you must first grab a secret id to retrieve the corresponding stub.

```python
#the secret variable come from the previous sample
stub = isss.getSecretPermissionStub(secret["id"])
stub["userId"] = 4
stub["secretAccessRoleName"] = "View"
stub.create()
```

Possible values for secretAccessRoleName are : "Owner", "View", "List", or "Edit"


### Creating a folder permission

To create a new permission for a specific folder, you must first grab a folder id to retrieve the corresponding stub.

```python
stub = isss.getFolderPermissionStub(isss.getFolder("Windows")[0]["id"])
stub["userId"] = 4
stub["folderAccessRoleName"] = "View"
stub.create()
```

Possible values for folderAccessRoleName are : "Owner", "View", "List", or "Edit"


### Creating a user

To create a new user, it's very similar, yet simpler :

```python
stub = isss.getUserStub()
stub["username"] = "lucifer"
stub["displayname"] = "Lucifer Morningstar"
stub["password"] = "Passw0rd"
stub.create()
```

### Creating a group

You should now be familiar with the concept...

```python
stub = isss.getGroupStub()
stub["name"] = "awesome people"
mygroup = stub.create() #keep a reference to the newly created group
```

As seen before, once your group is created you can store the result into a variable so you can start adding users

```python
mygroup.add("admin")
```

Caution, _add()_ is expecting **a numerical userId** or **a username**. _Not_ a search query !

# Updating things

Update works exactly like create, except your stub has already been created, so instead of calling create() you will call... well... update() 

### Updating a user

```python
u = isss.getUser(4)
u["password"] = "new password"
u.update()
```

### Updating a secret

```python
s = isss.getSecret(12)
s["name"] += " (updated)"
s.update()
```

### Updating a group

Group can be updated like any regular stub, but they also have 3 additionals methods.

A method to add a user into the group:

```python
isss.getGroup(2).add("admin") #using a search query - must return only 1 result
isss.getGroup(2).add(2) #or a userid
isss.getGroup(2).add("admin").add("romain") #tip: you can chain methods
```

A method to remove a user from the group:

```python
isss.getGroup(2).remove("admin")
isss.getGroup(2).remove(2) 
isss.getGroup(2).remove("admin").remove("romain")
```

And a method to list current users in the group:

```python
for user in isss.getGroup(2).getUsers():
	print user["id"]
```

Note : for performance reasons, the `getUsers()` method returns a list of IDs and usernames, **not a list of stubs**.

# Deleting things

While many things in Secret Server are never really deleted (we should rather say _disabled_), you can delete object from the server by calling the delete() function on the corresponding stub object

```python
#delete an existing stub
myUser.delete()
myGroup.delete()

#search & delete
isss.getSecret("foobar")[0].delete()
```

# Experimental APIs

For some reasons, Scripts APIs don't seem to be available as REST APIs, although they are available as SOAP APIs. For the sake of simplicity (I didn't want to mess with SOAP), the current implementation scraps the Web UI hence is likely to be broken at some point if you are not using the good version of Secret Server (tested on 10.6.000027 only)

To enable them, you'll need to add `True` to the ISSS constructor : 

```python
from isss import ISSS
isss = ISSS(
	"https://your.server.demo.com/SecretServer",
	"admin",
	"yourpassword", 
	True)
```

### Get all scripts metadata (PowerShell, SSH, SQL)

It's very easy to retrieve the list of available scripts. 

```python
#This function only returns script names and IDs
#Not the actual scripts content
scripts =  isss.getScriptList()

#Iterate over scripts, and grab & update their content
for script in scripts:
    if script.name == 'Test SSH':
        script = isss.getScript(script) # get the content
        script.content += "\n#automatically added by python"
        script.update()
```        
    
Of course if you know the id of a script, you can still grab it directly

```python
script =  isss.getScript(8)
script.content += "\n#automatically addedd by python"
script.update()
```

It worth noting that these scripts are not stub objects, like we have seen before.

### Scripts FileWatcher

OK there is a real need behind the crappy Script API that you've just discovered. I'm not expecting anyone to use it (especially since this API might stop working at some point), but if like me you are tired to edit your Heartbeat or Password Changer scripts from the web UI, you might be interested by this filewatcher command which depends on it.

From your shell, simply issue the following command : 

```
$ isss-fw https://server/SecretServer admin password directorypath
```

And it will start the filewatcher on the specified `directorypath` (which should be empty - the program will prompt you to delete its content if it's not)

If the directory doesn't exist, it will be created, and scripts will be automatically downloaded into it. Then any change to one of these file will be detected by the filewatcher and sent back to ISSS.

**Be careful**, it doesn't work with vim or any editor which are using temporary files. I'm using [brackets.io](http://brackets.io "brackets.io"), which works pretty well for me.

Also, you will quickly discover that (for now at least) you can't pass the current directory "." as the path parameter, so you will need to start the command from outside the directory you want to use. 
