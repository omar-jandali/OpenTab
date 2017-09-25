# the following is going to be a description of the error that I have been getting
# and cant seem to figure out how to fix.

# The issue is coming from the linking of a bank account through bank login with
# authentication. So as of right now, I am passing informatino through the request
# for the linking of the bank account, but no matter what I do I can't get it to work

# Before the snippets of code, I know that Synapse API uses the keywork 'USER' for
# all of the processing with new users within the API. I am working in Django,
# which also uses the default keyword 'USER' for creating users within the project.
# Because of that I imported the USER and saved it as SynapseUser.

# Here are all of the imports
from synapse_pay_rest import Client
from synapse_pay_rest import User as SynapseUser
from synapse_pay_rest.models.nodes import AchUsNode

# Here is the core of the issue which comes from teh login request and response

# the following is what will process
def authorizeLoginSynapse(request, form):
    # the following two lines grab the user and profile of the user that is
    # currently logged in to the Django Application.
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)

    # as of right now, I am taking the id for the new user that is created within
    # the synapse api and storing it locally in the database within the users
    # current profile so it is easy to the users informaiton.
    user_id = currentProfile.synapse_id
    # the following will send a reqest to a different method that will send a request
    # to grab the synapse users information and return the object that is returned
    synapseUser = retreiveUserSynapse(request)
    # i decided to enter generic parameters into the arguments just for testing
    # I just took the different parameters that I saw in the api documentation
    # to make sure that the code just works.
    bank_id = 'synapse_good'
    bank_pw = 'test1234'
    bank_code = 'fake'
    print(bank_code)
    print(bank_id)
    print(bank_pw)

    args = {
        'bank_name':bank_code,
        'username':bank_id,
        'password':bank_pw,
    }
    print(args)

    # The following is where the core of the problem comes from. WHen i send a new
    # request, It takes a few moments and then returns a n error. Here is the error
    # that keeps coming from this request and response that I am sending...
    # I have tried two different ways to send a request and I am getting two
    # different errors.

    # the first request is the following - I am passing an entire synapse user object
    # with the request.
    linked_account = AchUsNode.create_via_bank_login(synapseUser, **args)
    # the error that I get is the following

    # ValueError at /login_synapse/
    # The view tab.views.loginAccountSynapse didn't return an HttpResponse object. It returned None instead.
    # Request Method:	POST
    # Request URL:	http://127.0.0.1:8000/login_synapse/
    # Django Version:	1.11.5
    # Exception Type:	ValueError
    # Exception Value:
    # The view tab.views.loginAccountSynapse didn't return an HttpResponse object. It returned None instead.
    # Exception Location:	/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/django/core/handlers/base.py in _get_response, line 198

    # the following is the second type of request I send and get a different error.
    # with this request, I just send the synapse users stored ID which is assigned
    # to the user that is stored in the database.
    linked_account = AchUsNode.create_via_bank_login(user_id, **args)
    # the error that I get is the following

    # AttributeError at /login_synapse/
    # 'str' object has no attribute 'client'
    # Request Method:	POST
    # Request URL:	http://127.0.0.1:8000/login_synapse/
    # Django Version:	1.11.5
    # Exception Type:	AttributeError
    # Exception Value:
    # 'str' object has no attribute 'client'
    # Exception Location:	/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/synapse_pay_rest/models/nodes/ach_us_node.py in create_via_bank_login, line 39

    # I can not seem to figure out where this error is coming from or how to fix
    # the error so that I can authenticate the users login and connect a bank account
    # to the users profile.

    # the following will print the response that is received
    print(linked_account)
    # the following checks for mfa verification
    linked_account.mfa_verified
