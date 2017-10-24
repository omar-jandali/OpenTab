# the following method is going to be where all of the users synapse nodes will be
# requested and processed
def listedLinkAccounts(request):
    # the following grabs the currenly logged in users record and profile within
    # the application
    currentUser = loggedInUser(request)
    currentProfile = Profile.objects.get(user = currentUser)
    # the following will grab the users synapse id from the users local profile.
    user_id = currentProfile.synapse_id
    print(user_id)
    # the following will grab the entire synapse profile by sending an api request
    # with the users synapse profile.
    synapseUser = SynapseUser.by_id(client, str(user_id))
    # the following are options for how to display and structure the response for
    # all of the different nodes linked to the users account
    options = {
        'page':1,
        'per_page':20,
        'type': 'ACH-US',
    }
    # the following is the request and response with all of the users linked nodes
    # ready to be processed and storage of certain information.
    nodes = Node.all(synapseUser, **options)
    for node in nodes:
        print (node)
        print (type(node))

    return nodes
